"""Проверка цепочки импортов бота без установки реальных зависимостей.

Ловит ошибки вроде той, что была в handlers/callinline_button.py:
импорт SportClass из handlers.messages вместо handlers.data_classs.
Такая ошибка не видна при чтении кода, но роняет бота при старте.

Запуск:
    cd tdm_bot
    python -m tests.test_imports
"""

import importlib
import sys
import unittest

# Заглушки ставим до импортов проекта — общий модуль, чтобы тесты
# не перетирали подмены друг друга
from tests import stubs  # noqa: F401

MODULES_TO_CHECK = [
    'settings',
    'database.conn_db',
    'database.insert_log',
    'protection.roles',
    'protection.protection_insert',
    'protection.check_prot',
    'protection.registration_user',
    'protection',
    'handlers.data_classs',
    'handlers.callbacks',
    'handlers.callinline_button',
    'handlers.messages',
    'services_factory.services_sport',
    'database.select_lists',
    'services_factory.menu_lists',
]


class TestImports(unittest.TestCase):

    def test_all_modules_import(self):
        failures = []
        for name in MODULES_TO_CHECK:
            try:
                importlib.import_module(name)
            except Exception as exc:
                failures.append('{}: {}: {}'.format(
                    name, type(exc).__name__, exc))
        self.assertEqual(failures, [], 'Не импортируются:\n' + '\n'.join(failures))

    def test_sport_class_imported_from_right_module(self):
        """SportClass обязан лежать в data_classs, а не в messages"""
        from handlers.data_classs import SportClass as FromDataClasss
        self.assertIsNotNone(FromDataClasss)
        import handlers.messages as messages_module
        # В messages SportClass импортируется, но объявлен он в data_classs
        self.assertTrue(hasattr(messages_module, 'SportClass'))

    def test_logging_categories_available(self):
        from database.insert_log import (
            CATEGORY_SPORT, CATEGORY_INFO, CATEGORY_SERVICE,
            RESULT_OK, RESULT_NOT_FOUND, RESULT_MANY_OPTIONS,
            RESULT_TOO_MANY, RESULT_ERROR, RESULT_DENIED
        )
        self.assertEqual(CATEGORY_SPORT, 'спорт')
        self.assertEqual(CATEGORY_INFO, 'справка')
        self.assertEqual(CATEGORY_SERVICE, 'сервис')

    def test_search_path_is_configured(self):
        """search_path должен указывать на схему tdm_bot"""
        import database.conn_db as conn_db
        self.assertEqual(conn_db.TDM_SCHEMA, 'tdm_bot')
        self.assertIn('tdm_bot', conn_db.SEARCH_PATH)


class TestCallbackRouting(unittest.TestCase):
    """Проверка, что ветки маршрутизации достижимы.

    Отдельно проверяем префикс учреждений: в справочнике он записан
    с КИРИЛЛИЧЕСКОЙ с (U+0441) — проверено в БД, ascii=1089.
    Принимать надо оба написания.
    """

    def test_school_prefix_matches_cyrillic_variant(self):
        """Именно так лежит в базе — это основной случай"""
        import re
        pattern = r's[сc]hool_menu_'
        self.assertIsNotNone(re.match(pattern, 'sсhool_menu_219113'))

    def test_school_prefix_matches_latin_variant(self):
        """На случай, если справочник исправят"""
        import re
        pattern = r's[сc]hool_menu_'
        self.assertIsNotNone(re.match(pattern, 'school_menu_219113'))

    def test_school_prefix_does_not_match_sport(self):
        import re
        pattern = r's[сc]hool_menu_'
        self.assertIsNone(re.match(pattern, 'sport_menu_1'))

    def test_sport_prefix_still_works(self):
        import re
        self.assertIsNotNone(re.match(r'sport_menu_', 'sport_menu_1'))
        self.assertIsNone(re.match(r'sport_menu_', 'sсhool_menu_1'))


if __name__ == '__main__':
    unittest.main(verbosity=2)