# -*- coding: utf-8 -*-
import unittest
from lunar_python import Lunar, Solar


class JieQiTest(unittest.TestCase):
    def test7(self):
        lunar = Lunar.fromYmd(2012, 9, 1)
        self.assertEqual("2012-09-07 13:29:00", lunar.getJieQiTable()["白露"].toYmdHms())

    def test8(self):
        lunar = Lunar.fromYmd(2050, 12, 1)
        self.assertEqual("2050-12-07 06:41:00", lunar.getJieQiTable()["DA_XUE"].toYmdHms())

    def test1(self):
        solar = Solar.fromYmd(2021, 12, 21)
        lunar = solar.getLunar()
        self.assertEqual("冬至", lunar.getJieQi())
        self.assertEqual("", lunar.getJie())
        self.assertEqual("冬至", lunar.getQi())
