# -*- coding: utf-8 -*-
import unittest

from lunar_python import LunarYear


class YearTest(unittest.TestCase):

    def test1(self):
        year = LunarYear.fromYear(2017)
        self.assertEqual("二龙治水", year.getZhiShui())
        self.assertEqual("二人分饼", year.getFenBing())

    def test2(self):
        year = LunarYear.fromYear(2018)
        self.assertEqual("二龙治水", year.getZhiShui())
        self.assertEqual("八人分饼", year.getFenBing())

    def test3(self):
        year = LunarYear.fromYear(5)
        self.assertEqual("三龙治水", year.getZhiShui())
        self.assertEqual("一人分饼", year.getFenBing())

    def test4(self):
        year = LunarYear.fromYear(2021)
        self.assertEqual("十一牛耕田", year.getGengTian())

    def test5(self):
        year = LunarYear.fromYear(2018)
        self.assertEqual("三日得金", year.getDeJin())

    def test6(self):
        year = LunarYear.fromYear(1864)
        self.assertEqual("上元", year.getYuan())

    def test7(self):
        year = LunarYear.fromYear(1923)
        self.assertEqual("上元", year.getYuan())

    def test8(self):
        year = LunarYear.fromYear(1924)
        self.assertEqual("中元", year.getYuan())

    def test9(self):
        year = LunarYear.fromYear(1983)
        self.assertEqual("中元", year.getYuan())

    def test10(self):
        year = LunarYear.fromYear(1984)
        self.assertEqual("下元", year.getYuan())

    def test11(self):
        year = LunarYear.fromYear(2043)
        self.assertEqual("下元", year.getYuan())

    def test12(self):
        year = LunarYear.fromYear(1864)
        self.assertEqual("一运", year.getYun())

    def test13(self):
        year = LunarYear.fromYear(1883)
        self.assertEqual("一运", year.getYun())

    def test14(self):
        year = LunarYear.fromYear(1884)
        self.assertEqual("二运", year.getYun())

    def test15(self):
        year = LunarYear.fromYear(1903)
        self.assertEqual("二运", year.getYun())

    def test16(self):
        year = LunarYear.fromYear(1904)
        self.assertEqual("三运", year.getYun())

    def test17(self):
        year = LunarYear.fromYear(1923)
        self.assertEqual("三运", year.getYun())

    def test18(self):
        year = LunarYear.fromYear(2004)
        self.assertEqual("八运", year.getYun())
