# -*- coding: utf-8 -*-
import unittest

from lunar_python import Solar
from lunar_python.util import SolarUtil


class SolarTest(unittest.TestCase):
    def test(self):
        solar = Solar.fromYmd(2019, 5, 1)
        self.assertEqual("2019-05-01", solar.toString())
        self.assertEqual("2019-05-01 00:00:00 星期三 (劳动节) 金牛座", solar.toFullString())
        self.assertEqual("二〇一九年三月廿七", solar.getLunar().toString())
        self.assertEqual("二〇一九年三月廿七 己亥(猪)年 戊辰(龙)月 戊戌(狗)日 子(鼠)时 纳音[平地木 大林木 平地木 桑柘木] 星期三 西方白虎 星宿[参水猿](吉) 彭祖百忌[戊不受田田主不祥 戌不吃犬作怪上床] 喜神方位[巽](东南) 阳贵神方位[艮](东北) 阴贵神方位[坤](西南) 福神方位[艮](东北) 财神方位[坎](正北) 冲[(壬辰)龙] 煞[北]", solar.getLunar().toFullString())

    def test1(self):
        solar = Solar.fromYmdHms(2020, 5, 24, 13, 0, 0)
        self.assertEqual("二〇二〇年闰四月初二", solar.getLunar().toString())

    def test2(self):
        solar = Solar.fromYmd(11, 1, 1)
        self.assertEqual("一〇年腊月初八", solar.getLunar().toString())

    def test3(self):
        solar = Solar.fromYmd(11, 3, 1)
        self.assertEqual("一一年二月初八", solar.getLunar().toString())

    def test4(self):
        solar = Solar.fromYmd(26, 4, 13)
        self.assertEqual("二六年三月初八", solar.getLunar().toString())

    def test6(self):
        solar = Solar.fromYmd(1, 1, 1)
        self.assertEqual("0001-01-01", solar.toString())

    def test5(self):
        date = Solar.fromYmd(2020, 1, 23)
        self.assertEqual("2020-01-24", date.next(1).toString())
        # 仅工作日，跨越春节假期
        self.assertEqual("2020-02-03", date.next(1, True).toString())

        date = Solar.fromYmd(2020, 2, 3)
        self.assertEqual("2020-01-31", date.next(-3).toString())
        # 仅工作日，跨越春节假期
        self.assertEqual("2020-01-21", date.next(-3, True).toString())

        date = Solar.fromYmd(2020, 2, 9)
        self.assertEqual("2020-02-15", date.next(6).toString())
        # 仅工作日，跨越周末
        self.assertEqual("2020-02-17", date.next(6, True).toString())

        date = Solar.fromYmd(2020, 1, 17)
        self.assertEqual("2020-01-18", date.next(1).toString())
        # 仅工作日，周日调休按上班算
        self.assertEqual("2020-01-19", date.next(1, True).toString())

    def test10(self):
        self.assertEqual(True, SolarUtil.isLeapYear(1500))

    def test11(self):
        solar = Solar.fromYmd(2022, 3, 28)
        self.assertEqual("全国中小学生安全教育日", solar.getFestivals()[0])

    def test12(self):
        self.assertEqual("壬午", Solar.fromYmd(1991, 5, 12).getLunar().getDayInGanZhi())

    def test13(self):
        self.assertEqual("1582-09-30", Solar.fromYmd(1582, 10, 15).next(-5).toYmd())

    def test14(self):
        self.assertEqual("1582-10-04", Solar.fromYmd(1582, 10, 15).next(-1).toYmd())

    def test15(self):
        self.assertEqual("1582-09-29", Solar.fromYmd(1582, 10, 15).next(-6).toYmd())

    def test16(self):
        self.assertEqual(2, SolarUtil.getDaysBetween(100, 2, 28, 100, 3, 1))

    def test17(self):
        self.assertEqual(59, SolarUtil.getDaysInYear(100, 2, 28))

    def test18(self):
        self.assertEqual(61, SolarUtil.getDaysInYear(100, 3, 1))

    def test19(self):
        self.assertEqual("2023-09-30", Solar.fromYmd(2023, 8, 31).nextMonth(1).toYmd())

    def test20(self):
        self.assertEqual("2023-10-31", Solar.fromYmd(2023, 8, 31).nextMonth(2).toYmd())

    def test21(self):
        self.assertEqual("2024-02-29", Solar.fromYmd(2023, 8, 31).nextMonth(6).toYmd())

    def test22(self):
        self.assertEqual("2025-08-31", Solar.fromYmd(2023, 8, 31).nextYear(2).toYmd())
