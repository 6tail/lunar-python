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