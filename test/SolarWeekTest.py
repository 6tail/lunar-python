# -*- coding: utf-8 -*-
import unittest
from lunar_python import SolarMonth


class SolarWeekTest(unittest.TestCase):

    def test(self):
        month = SolarMonth.fromYm(2022, 12)
        self.assertEqual(5, len(month.getWeeks(0)))
