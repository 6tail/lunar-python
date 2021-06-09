# -*- coding: utf-8 -*-
import unittest
from lunar_python import Solar


class ShuJiuTest(unittest.TestCase):

    def test1(self):
        solar = Solar.fromYmd(2020, 12, 21)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertEqual("一九", shu_jiu.toString())
        self.assertEqual("一九第1天", shu_jiu.toFullString())

    def test2(self):
        solar = Solar.fromYmd(2020, 12, 22)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertEqual("一九", shu_jiu.toString())
        self.assertEqual("一九第2天", shu_jiu.toFullString())

    def test3(self):
        solar = Solar.fromYmd(2020, 1, 7)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertEqual("二九", shu_jiu.toString())
        self.assertEqual("二九第8天", shu_jiu.toFullString())

    def test4(self):
        solar = Solar.fromYmd(2021, 1, 6)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertEqual("二九", shu_jiu.toString())
        self.assertEqual("二九第8天", shu_jiu.toFullString())

    def test5(self):
        solar = Solar.fromYmd(2021, 1, 8)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertEqual("三九", shu_jiu.toString())
        self.assertEqual("三九第1天", shu_jiu.toFullString())

    def test6(self):
        solar = Solar.fromYmd(2021, 3, 5)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertEqual("九九", shu_jiu.toString())
        self.assertEqual("九九第3天", shu_jiu.toFullString())

    def test7(self):
        solar = Solar.fromYmd(2021, 7, 5)
        lunar = solar.getLunar()
        shu_jiu = lunar.getShuJiu()
        self.assertIsNone(shu_jiu)
