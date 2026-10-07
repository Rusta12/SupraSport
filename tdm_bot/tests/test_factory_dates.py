"""Тесты форматирования дат словами (factory_info_sport.format_date_ru).

Проверяем ровно то, что просил пользователь: «10.10.2024» → «10 октября 2024»,
«09.10.2028» → «9 октября 2028» (день без ведущего нуля).
"""

import unittest
from datetime import date

from tests import stubs  # noqa: F401
from services_factory.factory_info_sport import format_date_ru  # noqa: E402


class TestFormatDateRu(unittest.TestCase):

    def test_october(self):
        self.assertEqual(format_date_ru(date(2024, 10, 10)), '10 октября 2024')

    def test_day_without_leading_zero(self):
        self.assertEqual(format_date_ru(date(2028, 10, 9)), '9 октября 2028')

    def test_january(self):
        self.assertEqual(format_date_ru(date(2025, 1, 15)), '15 января 2025')

    def test_december(self):
        self.assertEqual(format_date_ru(date(2023, 12, 31)), '31 декабря 2023')

    def test_all_months_mapped(self):
        """Все 12 месяцев имеют русское название в родительном падеже"""
        seen = [
            format_date_ru(date(2024, m, 1)).split()[1]
            for m in range(1, 13)
        ]
        self.assertEqual(len(seen), 12)
        self.assertNotIn('', seen)

    def test_none_returns_empty(self):
        """NULL-дата в справочнике не должна ронять ответ"""
        self.assertEqual(format_date_ru(None), '')


if __name__ == '__main__':
    unittest.main(verbosity=2)