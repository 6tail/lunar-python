# -*- coding: utf-8 -*-
import unittest

from lunar_python import Solar


class WuHouTest(unittest.TestCase):

    def test1(self):
        solar = Solar.fromYmd(2020, 4, 23)
        lunar = solar.getLunar()
        self.assertEqual("萍始生", lunar.getWuHou())

    def test2(self):
        solar = Solar.fromYmd(2021, 1, 15)
        lunar = solar.getLunar()
        self.assertEqual("雉始雊", lunar.getWuHou())

    def test3(self):
        solar = Solar.fromYmd(2017, 1, 5)
        lunar = solar.getLunar()
        self.assertEqual("雁北乡", lunar.getWuHou())

    def test4(self):
        solar = Solar.fromYmd(2020, 4, 10)
        lunar = solar.getLunar()
        self.assertEqual("田鼠化为鴽", lunar.getWuHou())

    def test5(self):
        solar = Solar.fromYmd(2020, 6, 11)
        lunar = solar.getLunar()
        self.assertEqual("鵙始鸣", lunar.getWuHou())

    def test6(self):
        solar = Solar.fromYmd(2020, 6, 1)
        lunar = solar.getLunar()
        self.assertEqual("麦秋至", lunar.getWuHou())

    def test7(self):
        solar = Solar.fromYmd(2020, 12, 8)
        lunar = solar.getLunar()
        self.assertEqual("鹖鴠不鸣", lunar.getWuHou())

    def test8(self):
        solar = Solar.fromYmd(2020, 12, 11)
        lunar = solar.getLunar()
        self.assertEqual("鹖鴠不鸣", lunar.getWuHou())

    def test9(self):
        solar = Solar.fromYmd(1982, 12, 22)
        lunar = solar.getLunar()
        self.assertEqual("蚯蚓结", lunar.getWuHou())

    def test10(self):
        solar = Solar.fromYmd(2021, 12, 21)
        lunar = solar.getLunar()
        self.assertEqual("冬至 初候", lunar.getHou())

    def test11(self):
        solar = Solar.fromYmd(2021, 12, 26)
        lunar = solar.getLunar()
        self.assertEqual("冬至 二候", lunar.getHou())

    def test12(self):
        solar = Solar.fromYmd(2021, 12, 31)
        lunar = solar.getLunar()
        self.assertEqual("冬至 三候", lunar.getHou())

    def test13(self):
        solar = Solar.fromYmd(2022, 1, 5)
        lunar = solar.getLunar()
        self.assertEqual("小寒 初候", lunar.getHou())

    def test15(self):
        solar = Solar.fromYmd(2022, 8, 22)
        lunar = solar.getLunar()
        self.assertEqual("寒蝉鸣", lunar.getWuHou())

    def test16(self):
        solar = Solar.fromYmd(2022, 8, 23)
        lunar = solar.getLunar()
        self.assertEqual("鹰乃祭鸟", lunar.getWuHou())
