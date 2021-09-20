# -*- coding: utf-8 -*-
import unittest

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

    def test4(self):
        lunar = Lunar.fromYmd(1985, 12, 27)
        self.assertEqual("1995-11-05", lunar.getEightChar().getYun(1).getStartSolar().toYmd())

    def test5(self):
        lunar = Lunar.fromYmd(1985, 1, 27)
        self.assertEqual("1989-03-28", lunar.getEightChar().getYun(1).getStartSolar().toYmd())

    def test6(self):
        lunar = Lunar.fromYmd(1986, 12, 27)
        self.assertEqual("1990-04-15", lunar.getEightChar().getYun(1).getStartSolar().toYmd())
