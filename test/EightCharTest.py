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
        self.assertEqual("丁丑", lunar.getEightChar().getShenGong())

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
