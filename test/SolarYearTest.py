# -*- coding: utf-8 -*-
import unittest
from lunar_python import SolarYear


class SolarYearTest(unittest.TestCase):
    def test(self):
        year = SolarYear.fromYear(2019)
        self.assertEqual("2019", year.toString())
        self.assertEqual("2019年", year.toFullString())

        self.assertEqual("2020", year.next(1).toString())
        self.assertEqual("2020年", year.next(1).toFullString())
