# -*- coding: utf-8 -*-
import unittest
from lunar_python import Solar


class XunTest(unittest.TestCase):
    def testXun1(self):
        solar = Solar.fromYmdHms(2020, 11, 19, 0, 0, 0)
        lunar = solar.getLunar()
        self.assertEqual("甲午", lunar.getYearXun())

    def testXunKong1(self):
        solar = Solar.fromYmdHms(2020, 11, 19, 0, 0, 0)
        lunar = solar.getLunar()
        self.assertEqual("辰巳", lunar.getYearXunKong())
        self.assertEqual("午未", lunar.getMonthXunKong())
        self.assertEqual("戌亥", lunar.getDayXunKong())

    def testBaZiDayXunKong(self):
        solar = Solar.fromYmdHms(1990, 12, 23, 8, 37, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        self.assertEqual("子丑", eight_char.getDayXunKong())
