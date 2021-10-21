# -*- coding: utf-8 -*-
import unittest
from lunar_python import Lunar


class JieQiTest(unittest.TestCase):
    def test7(self):
        lunar = Lunar.fromYmd(2012, 9, 1)
        self.assertEqual("2012-09-07 13:29:00", lunar.getJieQiTable()["白露"].toYmdHms())

    def test8(self):
        lunar = Lunar.fromYmd(2050, 12, 1)
        self.assertEqual("2050-12-07 06:41:00", lunar.getJieQiTable()["大雪"].toYmdHms())
