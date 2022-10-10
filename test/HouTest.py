# -*- coding: utf-8 -*-
import unittest
from lunar_python import Solar


class HouTest(unittest.TestCase):

    def test1(self):
        solar = Solar.fromYmd(2021, 12, 21)
        self.assertEqual("冬至 初候", solar.getLunar().getHou())

    def test2(self):
        solar = Solar.fromYmd(2021, 12, 26)
        self.assertEqual("冬至 二候", solar.getLunar().getHou())

    def test3(self):
        solar = Solar.fromYmd(2021, 12, 31)
        self.assertEqual("冬至 三候", solar.getLunar().getHou())

    def test4(self):
        solar = Solar.fromYmd(2022, 1, 5)
        self.assertEqual("小寒 初候", solar.getLunar().getHou())
