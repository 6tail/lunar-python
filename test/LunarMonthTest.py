# -*- coding: utf-8 -*-
import unittest
from lunar_python import LunarMonth


class LunarMonthTest(unittest.TestCase):

    def test(self):
        month = LunarMonth.fromYm(2023, 1)
        self.assertEqual(1, month.getIndex())
        self.assertEqual("甲寅", month.getGanZhi())

    def test1(self):
        month = LunarMonth.fromYm(2023, -2)
        self.assertEqual(3, month.getIndex())
        self.assertEqual("丙辰", month.getGanZhi())

    def test2(self):
        month = LunarMonth.fromYm(2023, 3)
        self.assertEqual(4, month.getIndex())
        self.assertEqual("丁巳", month.getGanZhi())

    def test3(self):
        month = LunarMonth.fromYm(2024, 1)
        self.assertEqual(1, month.getIndex())
        self.assertEqual("丙寅", month.getGanZhi())

    def test4(self):
        month = LunarMonth.fromYm(2023, 12)
        self.assertEqual(13, month.getIndex())
        self.assertEqual("丙寅", month.getGanZhi())

    def test5(self):
        month = LunarMonth.fromYm(2022, 1)
        self.assertEqual(1, month.getIndex())
        self.assertEqual("壬寅", month.getGanZhi())
