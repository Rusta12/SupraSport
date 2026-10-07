"""Синхронизация ФИО и телефонов пользователей из состояний чатов API TDM.

Почему это нужно: события мессенджера не несут ФИО отправителя — в них
только sender_id (подтверждено на живом стенде и документацией SDK).
Единственный источник персональных данных — объект opponent в ответе
getAllUserGroupStates (он есть только у P2P-чатов; групповые не планируются).

Когда выполняется: при каждом запуске бота, из bot.py.
Как устроено, чтобы не тормозить:
  * сетевой запрос getAllUserGroupStates в любом случае делает Application.start()
    для поиска своего id — отдельного сетевого вызова НЕ добавляем,
    используем тот же bot._request;
  * имя и телефон сравниваются с текущими в базе;
  * UPDATE пишется только для пустых или изменившихся значений.
"""

import logging

from database.conn_db import (
    postgresql_to_dataframe,
    postgresql_to_data
)
from protection.protection_insert import to_user_id

logger = logging.getLogger(__name__)


def _format_fio(opponent: dict):
    """Сборка «Фамилия Имя Отчество» из объекта opponent.

    Пустые части (middleName у многих пуст) отбрасываются, лишние пробелы
    схлопываются. Если данных нет совсем — возвращается None.
    """
    if not isinstance(opponent, dict):
        return None

    parts = []
    for key in ('lastName', 'firstName', 'middleName'):
        value = opponent.get(key)
        if value:
            parts.append(str(value).strip())

    full = ' '.join(parts).strip()
    return full or None


def _format_phone(raw):
    """Приведение телефона к строке из цифр.

    Платформа отдаёт число без символов: 79035007657. Отбиваем только цифры —
    хранение единообразное, форматирование для красоты сделаем на выводе.
    """
    if raw is None:
        return None
    digits = ''.join(ch for ch in str(raw) if ch.isdigit())
    return digits or None


def collect_opponent_data(states) -> dict:
    """Собрать {id_пользователя: {'name': ФИО, 'phone': телефон}} из состояний.

    opponent есть только у P2P-чатов; состояния без opponent или без
    корректного id пропускаются. Поля, которых нет, — None.
    """
    collected = {}
    for state in states or []:
        opponent = state.get('opponent')
        if not isinstance(opponent, dict):
            continue

        user_id = to_user_id(opponent.get('id'))
        if user_id is None:
            continue

        collected[user_id] = {
            'name': _format_fio(opponent),
            'phone': _format_phone(opponent.get('phone')),
        }

    return collected


def sync_user_names(request) -> int:
    """Главная точка: вычитать состояния, обновить пустые/изменившиеся данные.

    :param request: экземпляр messenger_bot_api.util.Request (bot._request),
        сетевой вызов get_states() идёт через него.
    :return: число обновлённых (или добавленных) записей.
    """
    try:
        states = request.get_states()
    except Exception:
        logger.exception('Не удалось получить состояния чатов для синхронизации')
        return 0

    collected = collect_opponent_data(states)
    if not collected:
        logger.info('Синхронизация: states не дали ни одной записи opponent')
        return 0

    # Текущие имя/телефон из базы. Таблица реестра маленькая (аналитики),
    # полный SELECT дешевле и проще, чем ANY(%s).
    df = postgresql_to_dataframe(
        'SELECT id_user, messenger_name, phone FROM user_protection',
        ['id_user', 'messenger_name', 'phone']
    )
    current = {}
    for _, row in df.iterrows():
        current[int(row['id_user'])] = {
            'name': row['messenger_name'],
            'phone': row['phone'],
        }

    updated = 0
    for user_id, user_data in collected.items():
        exists = current.get(user_id)

        # Уже актуально — пропускаем запись совсем
        if exists and exists['name'] == user_data['name'] \
                and exists['phone'] == user_data['phone']:
            continue

        if exists is None:
            # Пользователь есть в состоянии чата, но не в реестре — регистрируем
            # с именем и телефоном (роль 1 по умолчанию). ON CONFLICT защитит
            # от гонки, если события успеют зарегистрировать его раньше.
            postgresql_to_data(
                """
                INSERT INTO user_protection (id_user, messenger_name, phone)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_user) DO NOTHING
                """,
                (user_id, user_data['name'], user_data['phone'])
            )
            logger.info('Синхронизация: добавлен пользователь %s (%s)',
                        user_id, user_data['name'])
        else:
            postgresql_to_data(
                """
                UPDATE user_protection
                SET messenger_name = %s, phone = %s
                WHERE id_user = %s
                """,
                (user_data['name'], user_data['phone'], user_id)
            )
            logger.info('Синхронизация: обновлён пользователь %s', user_id)
        updated += 1

    logger.info('Синхронизация завершена: обновлено %s записей', updated)
    return updated