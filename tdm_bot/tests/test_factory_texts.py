"""Тесты формулировок текстов factory_info_sport.

gs_phrase — строка о спортсменах, трудоустроенных в учреждении(-ях):
множественное число, если таких учреждений несколько.
"""

import unittest

from tests import stubs  # noqa: F401
from services_factory.factory_info_sport import gs_phrase  # noqa: E402


class TestGsPhrase(unittest.TestCase):

    def test_single_institution_singular(self):
        """Одно учреждение с трудоустроенными — «в учреждении»"""
        text = gs_phrase(gs_orgs=1, gs_total=7)
        self.assertIn('в учреждении', text)
        self.assertEqual(
            text,
            '– спортсмены, трудоустроенные в учреждении – [b]7 чел.[/b]'
        )

    def test_one_of_several_singular(self):
        """Из нескольких учреждений трудоустроенные есть только в одном — «в учреждении»"""
        text = gs_phrase(gs_orgs=1, gs_total=3)
        self.assertIn('в учреждении', text)
        self.assertNotIn('в учреждениях', text)

    def test_several_institutions_plural(self):
        """Несколько учреждений с трудоустроенными — «в учреждениях»"""
        text = gs_phrase(gs_orgs=3, gs_total=12)
        self.assertIn('в учреждениях', text)
        self.assertNotIn('в учреждении', text)

    def test_zero_total_hides_line(self):
        """Нет трудоустроенных — строка не выводится вообще"""
        self.assertEqual(gs_phrase(gs_orgs=0, gs_total=0), '')
        self.assertEqual(gs_phrase(gs_orgs=1, gs_total=0), '')


if __name__ == '__main__':
    unittest.main(verbosity=2)