# -*- coding: utf-8 -*-
import unittest
from lunar_python import SolarWeek, Solar
from lunar_python.util import SolarUtil


class WeekTest(unittest.TestCase):
    def test(self):
        # 一周的开始从星期一开始计
        start = 1
        week = SolarWeek.fromYmd(2019, 5, 1, start)
        self.assertEqual("2019.5.1", week.toString())
        self.assertEqual("2019年5月第1周", week.toFullString())
        # 当月共几周
        self.assertEqual(5, SolarUtil.getWeeksOfMonth(week.getYear(), week.getMonth(), start))
        # 当周第一天
        self.assertEqual("2019-04-29", week.getFirstDay().toString())
        # 当周第一天（本月）
        self.assertEqual("2019-05-01", week.getFirstDayInMonth().toString())

    def test1(self):
        # 一周的开始从星期日开始计
        start = 0
        week = SolarWeek.fromYmd(2019, 5, 1, start)
        self.assertEqual("2019.5.1", week.toString())
        self.assertEqual("2019年5月第1周", week.toFullString())
        # 当月共几周
        self.assertEqual(5, SolarUtil.getWeeksOfMonth(week.getYear(), week.getMonth(), start))
        # 当周第一天
        self.assertEqual("2019-04-28", week.getFirstDay().toString())
        # 当周第一天（本月）
        self.assertEqual("2019-05-01", week.getFirstDayInMonth().toString())

    def test2(self):
        week = SolarWeek.fromYmd(2022, 5, 1, 0)
        self.assertEqual(1, week.getIndex())

    def test3(self):
        week = SolarWeek.fromYmd(2022, 5, 7, 0)
        self.assertEqual(1, week.getIndex())

    def test4(self):
        week = SolarWeek.fromYmd(2022, 5, 8, 0)
        self.assertEqual(2, week.getIndex())

    def test5(self):
        week = SolarWeek.fromYmd(2022, 5, 1, 1)
        self.assertEqual(1, week.getIndex())

    def test6(self):
        week = SolarWeek.fromYmd(2022, 5, 2, 1)
        self.assertEqual(2, week.getIndex())

    def test7(self):
        week = SolarWeek.fromYmd(2022, 5, 8, 1)
        self.assertEqual(2, week.getIndex())

    def test8(self):
        week = SolarWeek.fromYmd(2021, 11, 1, 0)
        self.assertEqual(1, week.getIndex())

    def test9(self):
        week = SolarWeek.fromYmd(2021, 11, 1, 1)
        self.assertEqual(1, week.getIndex())

    def test10(self):
        week = SolarWeek.fromYmd(2021, 5, 2, 2)
        self.assertEqual(1, week.getIndex())

    def test11(self):
        week = SolarWeek.fromYmd(2021, 5, 4, 2)
        self.assertEqual(2, week.getIndex())

    def test12(self):
        week = SolarWeek.fromYmd(2022, 3, 6, 0)
        self.assertEqual(11, week.getIndexInYear())

    def test13(self):
        self.assertEqual(1, Solar.fromYmd(1582, 10, 1).getWeek())

    def test14(self):
        self.assertEqual(5, Solar.fromYmd(1582, 10, 15).getWeek())

    def test15(self):
        self.assertEqual(0, Solar.fromYmd(1129, 11, 17).getWeek())

    def test16(self):
        self.assertEqual(5, Solar.fromYmd(1129, 11, 1).getWeek())

    def test17(self):
        self.assertEqual(4, Solar.fromYmd(8, 11, 1).getWeek())

    def test18(self):
        self.assertEqual(0, Solar.fromYmd(1582, 9, 30).getWeek())

    def test19(self):
        self.assertEqual(1, Solar.fromYmd(1582, 1, 1).getWeek())

    def test20(self):
        self.assertEqual(6, Solar.fromYmd(1500, 2, 29).getWeek())

    def test21(self):
        self.assertEqual(3, Solar.fromYmd(9865, 7, 26).getWeek())

    def test22(self):
        self.assertEqual(6, Solar.fromYmd(1961, 9, 30).getWeek())
        self.assertEqual(6, Solar.fromYmdHms(1961, 9, 30, 0, 0, 0).getWeek())
        self.assertEqual(6, Solar.fromYmdHms(1961, 9, 30, 23, 59, 59).getWeek())

    def test23(self):
        self.assertEqual(3, Solar.fromYmd(2021, 9, 15).getWeek())
        self.assertEqual(3, Solar.fromYmdHms(2021, 9, 15, 0, 0, 0).getWeek())
        self.assertEqual(3, Solar.fromYmdHms(2021, 9, 15, 23, 59, 59).getWeek())
