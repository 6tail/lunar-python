# -*- coding: utf-8 -*-
import unittest
from lunar_python import SolarSeason


class SolarSeasonTest(unittest.TestCase):

    def test(self):
        season = SolarSeason.fromYm(2019, 5)
        self.assertEqual("2019.2", season.toString())
        self.assertEqual("2019年2季度", season.toFullString())
        self.assertEqual("2019.3", season.next(1).toString())
        self.assertEqual("2019年3季度", season.next(1).toFullString())
