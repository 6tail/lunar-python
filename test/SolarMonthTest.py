# -*- coding: utf-8 -*-
import unittest
from lunar_python import SolarMonth


class SolarMonthTest(unittest.TestCase):

    def test(self):
        month = SolarMonth.fromYm(2019, 5)
        self.assertEqual("2019-5", month.toString())
        self.assertEqual("2019年5月", month.toFullString())
        self.assertEqual("2019-6", month.next(1).toString())
        self.assertEqual("2019年6月", month.next(1).toFullString())
