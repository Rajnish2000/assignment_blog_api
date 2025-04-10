"""
Test for app module
"""

from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):

    def test_addition(self):
        res = calc.addition(5, 6)
        self.assertEqual(res, 11)

    def test_subtraction(self):
        res = calc.subtraction(20, 6)
        self.assertEqual(res, 14)

    def test_multiplication(self):
        res = calc.multiplication(13, 5)
        self.assertEqual(res, 65)
