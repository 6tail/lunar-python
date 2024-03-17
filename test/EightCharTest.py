# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from lunar_python import Solar, Lunar


class EightCharTest(unittest.TestCase):

    def test_gan_zhi(self):
        solar = Solar.fromYmdHms(2005, 12, 23, 8, 37, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        self.assertEqual("乙酉", eight_char.getYear())
        self.assertEqual("戊子", eight_char.getMonth())
        self.assertEqual("辛巳", eight_char.getDay())
        self.assertEqual("壬辰", eight_char.getTime())

    def test_shen_gong(self):
        lunar = Solar.fromYmdHms(1995, 12, 18, 10, 28, 0).getLunar()
        self.assertEqual("壬午", lunar.getEightChar().getShenGong())

    def test_shen_gong1(self):
        lunar = Solar.fromYmdHms(1994, 12, 6, 2, 0, 0).getLunar()
        self.assertEqual("乙丑", lunar.getEightChar().getShenGong())

    def test_shen_gong2(self):
        lunar = Solar.fromYmdHms(1990, 12, 11, 6, 0, 0).getLunar()
        self.assertEqual("庚辰", lunar.getEightChar().getShenGong())

    def test_shen_gong3(self):
        lunar = Solar.fromYmdHms(1993, 5, 23, 4, 0, 0).getLunar()
        self.assertEqual("庚申", lunar.getEightChar().getShenGong())

    def test4(self):
        lunar = Lunar.fromYmd(1985, 12, 27)
        self.assertEqual("1995-11-05", lunar.getEightChar().getYun(1).getStartSolar().toYmd())

    def test5(self):
        lunar = Lunar.fromYmd(1985, 1, 27)
        self.assertEqual("1989-03-28", lunar.getEightChar().getYun(1).getStartSolar().toYmd())

    def test6(self):
        lunar = Lunar.fromYmd(1986, 12, 27)
        self.assertEqual("1990-04-15", lunar.getEightChar().getYun(1).getStartSolar().toYmd())

    def test7(self):
        solar = Solar.fromYmdHms(2022, 8, 28, 1, 50, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        self.assertEqual("壬寅", eight_char.getYear())
        self.assertEqual("戊申", eight_char.getMonth())
        self.assertEqual("癸丑", eight_char.getDay())
        self.assertEqual("癸丑", eight_char.getTime())

    def test8(self):
        lunar = Lunar.fromYmdHms(2022, 8, 2, 1, 50, 0)
        eight_char = lunar.getEightChar()
        self.assertEqual("壬寅", eight_char.getYear())
        self.assertEqual("戊申", eight_char.getMonth())
        self.assertEqual("癸丑", eight_char.getDay())
        self.assertEqual("癸丑", eight_char.getTime())

    def test9(self):
        lunar = Lunar.fromDate(datetime.strptime('2022-08-28 01:50:00', '%Y-%m-%d %H:%M:%S'))
        eight_char = lunar.getEightChar()
        self.assertEqual("壬寅", eight_char.getYear())
        self.assertEqual("戊申", eight_char.getMonth())
        self.assertEqual("癸丑", eight_char.getDay())
        self.assertEqual("癸丑", eight_char.getTime())

    def test10(self):
        lunar = Solar.fromYmdHms(1988, 2, 15, 23, 30, 0).getLunar()
        eight_char = lunar.getEightChar()
        self.assertEqual("戊辰", eight_char.getYear())
        self.assertEqual("甲寅", eight_char.getMonth())
        self.assertEqual("庚子", eight_char.getDay())
        self.assertEqual("戊子", eight_char.getTime())

    def test11(self):
        lunar = Lunar.fromYmdHms(1987, 12, 28, 23, 30, 0)
        eight_char = lunar.getEightChar()
        self.assertEqual("戊辰", eight_char.getYear())
        self.assertEqual("甲寅", eight_char.getMonth())
        self.assertEqual("庚子", eight_char.getDay())
        self.assertEqual("戊子", eight_char.getTime())

    def test12(self):
        solar_list = Solar.fromBaZi("己卯", "辛未", "甲戌", "癸酉")
        self.assertLess(1, len(solar_list))

    def test13(self):
        lunar = Lunar.fromYmdHms(1991, 4, 5, 3, 37, 0)
        eight_char = lunar.getEightChar()
        self.assertEqual("辛未", eight_char.getYear())
        self.assertEqual("癸巳", eight_char.getMonth())
        self.assertEqual("戊子", eight_char.getDay())
        self.assertEqual("甲寅", eight_char.getTime())

    def test14(self):
        solar_list = Solar.fromBaZi("己卯", "辛未", "甲戌", "壬申")
        actual = []
        for solar in solar_list:
            actual.append(solar.toYmdHms())
        expected = ["1939-08-05 16:00:00", "1999-07-21 16:00:00"]
        self.assertListEqual(expected, actual)

    def test15(self):
        solar_list = Solar.fromBaZi("庚子", "戊子", "己卯", "庚午")
        actual = []
        for solar in solar_list:
            actual.append(solar.toYmdHms())
        expected = ["1901-01-01 12:00:00", "1960-12-17 12:00:00"]
        self.assertListEqual(expected, actual)

    def test16(self):
        solar_list = Solar.fromBaZi("癸卯", "甲寅", "癸丑", "甲子", 2, 1843)
        actual = []
        for solar in solar_list:
            actual.append(solar.toYmdHms())
        expected = ["1843-02-08 23:00:00", "2023-02-24 23:00:00"]
        self.assertListEqual(expected, actual)

    def test17(self):
        solar_list = Solar.fromBaZi("己亥", "丁丑", "壬寅", "戊申")
        actual = []
        for solar in solar_list:
            actual.append(solar.toYmdHms())
        expected = ["1900-01-29 16:00:00", "1960-01-15 16:00:00"]
        self.assertListEqual(expected, actual)

    def test18(self):
        solar_list = Solar.fromBaZi("己亥", "丙子", "癸酉", "庚申")
        actual = []
        for solar in solar_list:
            actual.append(solar.toYmdHms())
        expected = ["1959-12-17 16:00:00"]
        self.assertListEqual(expected, actual)

    def test19(self):
        solar_list = Solar.fromBaZi("丁卯", "丁未", "甲申", "乙丑", 1, 1900)
        actual = []
        for solar in solar_list:
            actual.append(solar.toYmdHms())
        expected = ["1987-08-03 02:00:00"]
        self.assertListEqual(expected, actual)
