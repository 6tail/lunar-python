# -*- coding: utf-8 -*-
import unittest
from lunar_python import Solar


class XingZuoTest(unittest.TestCase):

    def test1(self):
        solar = Solar.fromYmd(2020, 3, 21)
        self.assertEqual("白羊", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 4, 19)
        self.assertEqual("白羊", solar.getXingZuo())

    def test2(self):
        solar = Solar.fromYmd(2020, 4, 20)
        self.assertEqual("金牛", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 5, 20)
        self.assertEqual("金牛", solar.getXingZuo())

    def test3(self):
        solar = Solar.fromYmd(2020, 5, 21)
        self.assertEqual("双子", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 6, 21)
        self.assertEqual("双子", solar.getXingZuo())

    def test4(self):
        solar = Solar.fromYmd(2020, 6, 22)
        self.assertEqual("巨蟹", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 7, 22)
        self.assertEqual("巨蟹", solar.getXingZuo())

    def test5(self):
        solar = Solar.fromYmd(2020, 7, 23)
        self.assertEqual("狮子", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 8, 22)
        self.assertEqual("狮子", solar.getXingZuo())

    def test6(self):
        solar = Solar.fromYmd(2020, 8, 23)
        self.assertEqual("处女", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 9, 22)
        self.assertEqual("处女", solar.getXingZuo())

    def test7(self):
        solar = Solar.fromYmd(2020, 9, 23)
        self.assertEqual("天秤", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 10, 23)
        self.assertEqual("天秤", solar.getXingZuo())

    def test8(self):
        solar = Solar.fromYmd(2020, 10, 24)
        self.assertEqual("天蝎", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 11, 22)
        self.assertEqual("天蝎", solar.getXingZuo())

    def test9(self):
        solar = Solar.fromYmd(2020, 11, 23)
        self.assertEqual("射手", solar.getXingZuo())
        solar = Solar.fromYmd(2020, 12, 21)
        self.assertEqual("射手", solar.getXingZuo())

    def test10(self):
        solar = Solar.fromYmd(2020, 12, 22)
        self.assertEqual("摩羯", solar.getXingZuo())
        solar = Solar.fromYmd(2021, 1, 19)
        self.assertEqual("摩羯", solar.getXingZuo())

    def test11(self):
        solar = Solar.fromYmd(2021, 1, 20)
        self.assertEqual("水瓶", solar.getXingZuo())
        solar = Solar.fromYmd(2021, 2, 18)
        self.assertEqual("水瓶", solar.getXingZuo())

    def test12(self):
        solar = Solar.fromYmd(2021, 2, 19)
        self.assertEqual("双鱼", solar.getXingZuo())
        solar = Solar.fromYmd(2021, 3, 20)
        self.assertEqual("双鱼", solar.getXingZuo())
