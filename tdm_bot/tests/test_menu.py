"""Тесты механизма меню-списков: xlsx в памяти и маршрутизация кнопок.

Внешние зависимости подменяются (tests.stubs), реальные pandas/openpyxl
не нужны: сериализация проверяется через подмену df.
"""

import unittest

from tests import stubs  # noqa: F401


class _FakeDataFrame:
    """Минимум DataFrame, который умеет писать байты в буфер"""

    def __init__(self, rows=2):
        self.rows = rows

    @property
    def shape(self):
        return (self.rows, 0)

    def to_excel(self, buffer, **kwargs):
        buffer.write(b'PK\x03\x04example-xlsx-content')


class TestXlsxFile(unittest.TestCase):

    def test_returns_file_with_name_and_bytes(self):
        from services_factory.menu_lists import _xlsx_file
        file_obj = _xlsx_file(_FakeDataFrame(), 'Список_организаций')

        self.assertTrue(file_obj.name.startswith('Список_организаций_'))
        self.assertTrue(file_obj.name.endswith('.xlsx'))
        # валидный xlsx начинается с сигнатуры zip
        self.assertEqual(file_obj.content[:2], b'PK')
        self.assertGreater(len(file_obj.content), 10)

    def test_different_base_name(self):
        from services_factory.menu_lists import _xlsx_file
        file_obj = _xlsx_file(_FakeDataFrame(), 'Список_федераций')
        self.assertTrue(file_obj.name.startswith('Список_федераций_'))


class TestMenuRouting(unittest.TestCase):
    """callback_data кнопок меню ведёт на правильные сервисы"""

    def test_org_moskomport_route(self):
        from unittest import mock
        import handlers.callbacks as callbacks

        event = object()
        with mock.patch.object(callbacks, 'send_organizations_msk_list') as handler:
            callbacks.mean_allocation(event, 'list_org_moskomport')
        handler.assert_called_once_with(event)

    def test_org_other_route(self):
        from unittest import mock
        import handlers.callbacks as callbacks

        event = object()
        with mock.patch.object(callbacks, 'send_organizations_other_list') as handler:
            callbacks.mean_allocation(event, 'list_org_other')
        handler.assert_called_once_with(event)

    def test_federations_route(self):
        from unittest import mock
        import handlers.callbacks as callbacks

        event = object()
        with mock.patch.object(callbacks, 'send_federations_list') as handler:
            callbacks.mean_allocation(event, 'list_federations')
        handler.assert_called_once_with(event)

    def test_other_callbacks_not_intercepted(self):
        """кнопки меню не должны ловить спортивные callback_data"""
        from unittest import mock
        import handlers.callbacks as callbacks

        with mock.patch.object(callbacks, 'send_organizations_msk_list') as org_m, \
                mock.patch.object(callbacks, 'send_organizations_other_list') as org_o, \
                mock.patch.object(callbacks, 'send_federations_list') as fed, \
                mock.patch.object(callbacks, 'print_sport') as sport, \
                mock.patch.object(callbacks, 'print_school') as school:
            callbacks.mean_allocation(object(), 'sport_menu_12')
        org_m.assert_not_called()
        org_o.assert_not_called()
        fed.assert_not_called()
        sport.assert_called_once()
        school.assert_not_called()


class TestSendEmptyTable(unittest.TestCase):
    """Пустой список → текстовое сообщение, без файла"""

    def _make_event(self):
        replies = []
        event = type('Ev', (), {
            'reply_text': lambda self, t: replies.append(t),
            'reply_file_message': lambda self, *a: replies.append(('file', a)),
            'sender_id': 1,
        })()
        return event, replies

    def test_empty_df_answers_text(self):
        from services_factory.menu_lists import _send_table
        event, replies = self._make_event()
        ok = _send_table(event, _FakeDataFrame(rows=0), 'Список', 'Вступление')
        self.assertFalse(ok)
        self.assertEqual(len(replies), 1)
        self.assertIsInstance(replies[0], str)


class TestMimeWorkaround(unittest.TestCase):
    """Регрессия: без ворк-аунда .xlsx уходит с mimeType=None,
    и платформа отвечает 400 REQUIRED_FIELD_BLANK file.mimeType."""

    def test_workaround_gives_mime_for_xlsx(self):
        import mimetypes
        from mime_types import apply_mime_workaround

        apply_mime_workaround()
        mime = mimetypes.MimeTypes().guess_type('Список_организаций_2026-10-07.xlsx')[0]
        self.assertEqual(
            mime,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_workaround_idempotent(self):
        from mime_types import apply_mime_workaround
        apply_mime_workaround()
        apply_mime_workaround()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)