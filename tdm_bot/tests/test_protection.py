"""Тесты логики прав и журнала без обращения к БД.

Запуск:
    cd tdm_bot
    python -m tests.test_protection

Зависимости (pandas, psycopg2, messenger_bot_api) в тестах не нужны —
они подменяются заглушками, потому что проверяется чистая логика:
разбор payload, роли, обрезка текста, тексты ответов.
"""

import sys
import unittest

# Общие заглушки: оба тест-модуля используют один набор подмен
from tests import stubs  # noqa: F401

# --- импорты проекта --------------------------------------------------
from protection.roles import (  # noqa: E402
    ROLE_ANALYTIC, ROLE_SENIOR_ANALYTIC, ROLE_NAMES, role_name, is_valid_role
)
from protection.registration_user import (  # noqa: E402
    extract_user_data, cache_user_profile, user_cache,
    profile_user_print
)
from protection.protection_insert import to_user_id  # noqa: E402
from database.insert_log import truncate_text, MAX_TEXT_LENGTH  # noqa: E402


class FakeEvent:
    """Минимальное событие для проверки текстов"""

    def __init__(self, sender_id=1001, workspace_id=1, group_id=2):
        self.sender_id = sender_id
        self.workspace_id = workspace_id
        self.group_id = group_id
        self.replies = []

    def reply_text(self, text):
        self.replies.append(text)


class TestRoles(unittest.TestCase):

    def test_analyst_is_base_role(self):
        self.assertEqual(ROLE_ANALYTIC, 1)

    def test_senior_role_is_two(self):
        self.assertEqual(ROLE_SENIOR_ANALYTIC, 2)

    def test_there_is_no_zero_role(self):
        """Состояния «без доступа» в системе не существует"""
        self.assertNotIn(0, ROLE_NAMES)

    def test_role_name_known(self):
        self.assertEqual(role_name(1), 'Аналитик')
        self.assertEqual(role_name(2), 'Старший аналитик')

    def test_role_name_unknown_does_not_crash(self):
        self.assertIn('0', role_name(0))

    def test_is_valid_role(self):
        self.assertTrue(is_valid_role(1))
        self.assertTrue(is_valid_role(2))
        self.assertFalse(is_valid_role(0))
        self.assertFalse(is_valid_role(99))


class TestUserIdCoercion(unittest.TestCase):
    """Идентификаторы приходят из разных событий и могут быть строками"""

    def test_int_passthrough(self):
        self.assertEqual(to_user_id(1001), 1001)

    def test_string_converted(self):
        self.assertEqual(to_user_id('1001'), 1001)

    def test_none(self):
        self.assertIsNone(to_user_id(None))

    def test_garbage_returns_none(self):
        """Мусорный id не должен ронять обработку — возвращаем None,
        и вызывающий код пропустит операцию"""
        self.assertIsNone(to_user_id('не число'))


class TestExtractUserData(unittest.TestCase):
    """payload.user в TDM: набор ключей требует проверки на стенде (T-02),
    поэтому разбираем несколько вариантов написания"""

    def test_camel_case(self):
        data = extract_user_data({
            'id': 555, 'fullName': 'Иванов Иван',
            'email': 'ivanov@example.com', 'phone': '+79991234567'
        })
        self.assertEqual(data['user_id'], 555)
        self.assertEqual(data['name'], 'Иванов Иван')
        self.assertEqual(data['email'], 'ivanov@example.com')
        self.assertEqual(data['phone'], '+79991234567')

    def test_snake_and_short_keys(self):
        data = extract_user_data({
            'userId': '777', 'name': 'Петров', 'mail': 'p@example.com'
        })
        self.assertEqual(data['user_id'], 777)
        self.assertEqual(data['name'], 'Петров')
        self.assertEqual(data['email'], 'p@example.com')
        # У TDM нет логина/ника — колонка username удалена из схемы
        self.assertNotIn('username', data)

    def test_empty_and_null_values_skipped(self):
        """Пустые строки и 'null' считаются отсутствием значения,
        иначе обновление затрёт уже сохранённое ФИО"""
        data = extract_user_data({'id': 1, 'name': '', 'email': 'null'})
        self.assertIsNone(data['name'])
        self.assertIsNone(data['email'])

    def test_not_a_dict(self):
        self.assertEqual(extract_user_data(None), {})
        self.assertEqual(extract_user_data('строка'), {})

    def test_missing_id(self):
        data = extract_user_data({'name': 'Без идентификатора'})
        self.assertIsNone(data['user_id'])


class TestUserCache(unittest.TestCase):

    def setUp(self):
        user_cache.clear()

    def test_cache_stores_profile(self):
        cache_user_profile({'id': 42, 'name': 'Сидоров'})
        self.assertEqual(user_cache[42]['name'], 'Сидоров')

    def test_cache_merges_new_fields(self):
        """Позднее событие может принести e-mail — прежнее ФИО не теряется"""
        cache_user_profile({'id': 42, 'name': 'Сидоров'})
        cache_user_profile({'id': 42, 'email': 's@example.com'})
        self.assertEqual(user_cache[42]['name'], 'Сидоров')
        self.assertEqual(user_cache[42]['email'], 's@example.com')

    def test_cache_ignores_payload_without_id(self):
        cache_user_profile({'name': 'Без id'})
        self.assertEqual(user_cache, {})


class TestSyncNames(unittest.TestCase):
    """ФИО берётся из opponent состояний чатов — событийного источника имён нет.

    Проверяем чистую логику: сборку ФИО и сбор словаря из состояний.
    Сетевой вызов и запись в БД в тестах не участвуют.
    """

    def test_fio_with_middle_name(self):
        from protection.sync_names import _format_fio
        fio = _format_fio({
            'id': 1, 'lastName': 'Булгаков', 'firstName': 'Рустам',
            'middleName': 'Анатольевич'
        })
        self.assertEqual(fio, 'Булгаков Рустам Анатольевич')

    def test_fio_without_middle_name(self):
        from protection.sync_names import _format_fio
        fio = _format_fio({
            'id': 1, 'lastName': 'Ратников', 'firstName': 'Антон',
            'middleName': ''
        })
        self.assertEqual(fio, 'Ратников Антон')

    def test_fio_whitespace_collapsed(self):
        from protection.sync_names import _format_fio
        fio = _format_fio({
            'lastName': '  Иванов ', 'firstName': ' Иван ', 'middleName': ''
        })
        self.assertEqual(fio, 'Иванов Иван')

    def test_fio_empty_returns_none(self):
        from protection.sync_names import _format_fio
        self.assertIsNone(_format_fio({}))
        self.assertIsNone(_format_fio(None))
        self.assertIsNone(_format_fio({'id': 7}))

    def test_phone_digits_only(self):
        from protection.sync_names import _format_phone
        self.assertEqual(_format_phone(79035007657), '79035007657')
        self.assertEqual(_format_phone('7 903 500-76-57'), '79035007657')
        self.assertIsNone(_format_phone(None))
        self.assertIsNone(_format_phone(''))

    def test_collect_opponents_from_states(self):
        from protection.sync_names import collect_opponent_data
        states = [
            # P2P-чат с пользователем
            {'groupId': 1, 'opponent': {
                'id': '2715476478492067', 'lastName': 'Булгаков',
                'firstName': 'Рустам', 'middleName': '',
                'phone': 79035007657
            }},
            # Системный чат — opponent нет
            {'groupId': -55},
            # Бот сам себе? opponent без id
            {'groupId': 2, 'opponent': {'firstName': 'Без id'}},
        ]
        collected = collect_opponent_data(states)
        self.assertEqual(
            collected,
            {2715476478492067: {
                'name': 'Булгаков Рустам',
                'phone': '79035007657'
            }}
        )

    def test_collect_skips_missing_phone(self):
        from protection.sync_names import collect_opponent_data
        states = [{'groupId': 1, 'opponent': {
            'id': 5, 'lastName': 'Иванов', 'firstName': 'Иван'
        }}]
        collected = collect_opponent_data(states)
        self.assertIsNone(collected[5]['phone'])

    def test_collect_empty(self):
        from protection.sync_names import collect_opponent_data
        self.assertEqual(collect_opponent_data([]), {})
        self.assertEqual(collect_opponent_data(None), {})


class TestFillProfileFromChat(unittest.TestCase):
    """Дозаполнение имени/телефона при первом контакте.

    Реальный сетевой вызов get_state и запись в БД подменяются.
    """

    def _repo_user(self, user_id):
        """Профили, «находящиеся» в БД в рамках этого теста"""
        profile = self._db.get(user_id)
        if profile is None:
            return None
        return {
            'id_user': user_id,
            'messenger_name': profile.get('messenger_name'),
            'phone': profile.get('phone'),
            'id_role_access': 1,
            'created_at': None,
            'arhiv': False,
        }

    def setUp(self):
        from unittest import mock
        self.mock = mock
        import protection.registration_user as ru
        import database.conn_db as conn_db
        self.ru = ru
        self._db = {}
        ru.user_cache.clear()
        # get_user_profile читает БД через наш словарь
        self._orig_get_profile = ru.get_user_profile
        ru.get_user_profile = lambda uid: self._repo_user(uid)
        # запись в БД перехватываем
        self._sql_calls = []
        self._orig_to_data = conn_db.postgresql_to_data

        def fake_to_data(query, params):
            self._sql_calls.append((query, params))
            # эмуляция UPDATE messenger_name/phone
            if 'SET messenger_name' in query:
                uid = params[2]
                rec = self._db.setdefault(uid, {})
                for idx, col in ((0, 'messenger_name'), (1, 'phone')):
                    value = params[idx]
                    if value:
                        rec[col] = value

        conn_db.postgresql_to_data = fake_to_data

    def tearDown(self):
        import database.conn_db as conn_db
        self.ru.get_user_profile = self._orig_get_profile
        conn_db.postgresql_to_data = self._orig_to_data

    def _event(self, ws=-1, gid=7, state_opponent=None):
        request = type('FakeRequest', (), {
            'get_state': lambda self, w, g: (
                {'groupId': g, 'opponent': state_opponent}
                if state_opponent else {}
            )
        })()
        return type('FakeEvent', (), {
            '_request': request,
            'workspace_id': ws,
            'group_id': gid,
            'sender_id': 42,
        })()

    def test_fill_writes_name_and_phone(self):
        from protection.registration_user import fill_profile_from_chat
        ok = fill_profile_from_chat(
            self._event(state_opponent={
                'id': 42, 'lastName': 'Иванов', 'firstName': 'Иван',
                'middleName': '', 'phone': 79030000000
            }), 42)
        self.assertTrue(ok)
        self.assertEqual(self._db[42]['messenger_name'], 'Иванов Иван')
        self.assertEqual(self._db[42]['phone'], '79030000000')
        self.assertEqual(self.ru.user_cache[42]['name'], 'Иванов Иван')

    def test_fill_without_opponent_no_write(self):
        from protection.registration_user import fill_profile_from_chat
        ok = fill_profile_from_chat(self._event(state_opponent=None), 42)
        self.assertFalse(ok)
        self.assertEqual(self._sql_calls, [])
        self.assertNotIn(42, self._db)

    def test_fill_unknown_opponent_skips(self):
        from protection.registration_user import fill_profile_from_chat
        ok = fill_profile_from_chat(self._event(state_opponent={
            'id': 777, 'lastName': 'Другой', 'firstName': 'Человек'
        }), 42)
        self.assertFalse(ok)
        self.assertNotIn(42, self._db)

    def test_register_event_user_fills_new_user(self):
        """Сквозной сценарий: первый контакт → имя из состояния чата"""
        import protection.registration_user as ru
        state_opponent = {
            'id': 42, 'lastName': 'Иванов', 'firstName': 'Иван',
            'middleName': '', 'phone': 79030000000
        }
        event = self._event(state_opponent=state_opponent)

        with self.mock.patch.object(ru, 'register_user_by_id',
                                    return_value=True) as m_reg:
            ru.register_event_user(event)

        m_reg.assert_called_once()
        self.assertEqual(self._db[42]['messenger_name'], 'Иванов Иван')
        self.assertEqual(self._db[42]['phone'], '79030000000')

    def test_name_present_skips_chat_fetch(self):
        """Пользователь с именем не опрашивает состояние чата заново"""
        import protection.registration_user as ru
        self._db[42] = {'messenger_name': 'Иванов Иван'}
        with self.mock.patch.object(ru, 'fill_profile_from_chat') as m_fill:
            ru.register_event_user(self._event(state_opponent=None))
        m_fill.assert_not_called()


class TestTruncateText(unittest.TestCase):

    def test_short_text_unchanged(self):
        self.assertEqual(truncate_text('баскетбол'), 'баскетбол')

    def test_none_passthrough(self):
        self.assertIsNone(truncate_text(None))

    def test_long_text_cut(self):
        text = 'а' * 900
        self.assertEqual(len(truncate_text(text)), MAX_TEXT_LENGTH)

    def test_exactly_at_limit(self):
        text = 'а' * MAX_TEXT_LENGTH
        self.assertEqual(truncate_text(text), text)


class TestProfileText(unittest.TestCase):
    """Проверка текстов без БД: подменяем get_user_profile"""

    def setUp(self):
        import protection.registration_user as ru
        self._orig = ru.get_user_profile
        self._profile = None

        def fake_profile(user_id):
            return self._profile

        ru.get_user_profile = fake_profile

    def tearDown(self):
        import protection.registration_user as ru
        ru.get_user_profile = self._orig

    def test_unknown_user_gets_hint(self):
        """Отсутствие записи не должно выглядеть как ошибка"""
        self._profile = None
        text = profile_user_print(FakeEvent(sender_id=999))
        self.assertIn('не найден', text)
        self.assertIn('/start', text)

    def test_analyst_profile(self):
        from datetime import datetime
        self._profile = {
            'id_user': 1001,
            'messenger_name': 'Иванов Иван',
            'id_role_access': 1,
            'created_at': datetime(2026, 1, 15, 9, 30),
            'arhiv': False,
        }
        text = profile_user_print(FakeEvent(sender_id=1001))
        self.assertIn('Иванов Иван', text)
        self.assertIn('Аналитик', text)
        self.assertIn('15.01.2026', text)
        self.assertIn('активный', text)

    def test_analyst_is_hinted_about_senior_role(self):
        self._profile = {
            'id_user': 1, 'messenger_name': 'X', 'id_role_access': 1,
            'created_at': None, 'arhiv': False,
        }
        text = profile_user_print(FakeEvent(sender_id=1))
        self.assertIn('Старший аналитик', text)

    def test_senior_has_no_hint(self):
        self._profile = {
            'id_user': 1, 'messenger_name': 'X', 'id_role_access': 2,
            'created_at': None, 'arhiv': False,
        }
        text = profile_user_print(FakeEvent(sender_id=1))
        self.assertIn('Старший аналитик', text)
        self.assertNotIn('выдаётся по обращению', text)

    def test_archived_user_marked(self):
        self._profile = {
            'id_user': 1, 'messenger_name': 'X', 'id_role_access': 1,
            'created_at': None, 'arhiv': True,
        }
        text = profile_user_print(FakeEvent(sender_id=1))
        self.assertIn('архивный', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)