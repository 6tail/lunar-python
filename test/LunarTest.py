# -*- coding: utf-8 -*-
import unittest
from lunar_python import Lunar, Solar


class LunarTest(unittest.TestCase):

    def test(self):
        date = Lunar.fromYmdHms(2019, 3, 27, 0, 0, 0)
        self.assertEqual("二〇一九年三月廿七", date.toString())
        self.assertEqual("二〇一九年三月廿七 己亥(猪)年 戊辰(龙)月 戊戌(狗)日 子(鼠)时 纳音[平地木 大林木 平地木 桑柘木] 星期三 (七殿泰山王诞) 西方白虎 星宿[参水猿](吉) 彭祖百忌[戊不受田田主不祥 戌不吃犬作怪上床] 喜神方位[巽](东南) 阳贵神方位[艮](东北) 阴贵神方位[坤](西南) 福神方位[坎](正北) 财神方位[坎](正北) 冲[(壬辰)龙] 煞[北]", date.toFullString())
        self.assertEqual("2019-05-01", date.getSolar().toString())
        self.assertEqual("2019-05-01 00:00:00 星期三 (劳动节) 金牛座", date.getSolar().toFullString())

    def test1(self):
        solar = Solar.fromYmdHms(100, 1, 1, 12, 0, 0)
        self.assertEqual("九九年腊月初二", solar.getLunar().toString())

    def test2(self):
        solar = Solar.fromYmdHms(3218, 12, 31, 12, 0, 0)
        self.assertEqual("三二一八年冬月廿二", solar.getLunar().toString())

    def test3(self):
        lunar = Lunar.fromYmdHms(5, 1, 6, 12, 0, 0)
        self.assertEqual("0005-02-03", lunar.getSolar().toString())

    def test4(self):
        lunar = Lunar.fromYmdHms(9998, 12, 2, 12, 0, 0)
        self.assertEqual("9999-01-11", lunar.getSolar().toString())

    def test5(self):
        lunar = Lunar.fromYmdHms(1905, 1, 1, 12, 0, 0)
        self.assertEqual("1905-02-04", lunar.getSolar().toString())

    def test6(self):
        lunar = Lunar.fromYmdHms(2038, 12, 29, 12, 0, 0)
        self.assertEqual("2039-01-23", lunar.getSolar().toString())

    def test7(self):
        lunar = Lunar.fromYmdHms(2020, -4, 2, 13, 0, 0)
        self.assertEqual("二〇二〇年闰四月初二", lunar.toString())
        self.assertEqual("2020-05-24", lunar.getSolar().toString())

    def test8(self):
        lunar = Lunar.fromYmdHms(2020, 12, 10, 13, 0, 0)
        self.assertEqual("二〇二〇年腊月初十", lunar.toString())
        self.assertEqual("2021-01-22", lunar.getSolar().toString())

    def test9(self):
        lunar = Lunar.fromYmdHms(1500, 1, 1, 12, 0, 0)
        self.assertEqual("1500-01-31", lunar.getSolar().toString())

    def test10(self):
        lunar = Lunar.fromYmdHms(1500, 12, 29, 12, 0, 0)
        self.assertEqual("1501-01-18", lunar.getSolar().toString())

    def test11(self):
        solar = Solar.fromYmdHms(1500, 1, 1, 12, 0, 0)
        self.assertEqual("一四九九年腊月初一", solar.getLunar().toString())

    def test12(self):
        solar = Solar.fromYmdHms(1500, 12, 31, 12, 0, 0)
        self.assertEqual("一五〇〇年腊月十一", solar.getLunar().toString())

    def test13(self):
        solar = Solar.fromYmdHms(1582, 10, 4, 12, 0, 0)
        self.assertEqual("一五八二年九月十八", solar.getLunar().toString())

    def test14(self):
        solar = Solar.fromYmdHms(1582, 10, 15, 12, 0, 0)
        self.assertEqual("一五八二年九月十九", solar.getLunar().toString())

    def test15(self):
        lunar = Lunar.fromYmdHms(1582, 9, 18, 12, 0, 0)
        self.assertEqual("1582-10-04", lunar.getSolar().toString())

    def test16(self):
        lunar = Lunar.fromYmdHms(1582, 9, 19, 12, 0, 0)
        self.assertEqual("1582-10-15", lunar.getSolar().toString())

    def test17(self):
        lunar = Lunar.fromYmdHms(2019, 12, 12, 11, 22, 0)
        self.assertEqual("2020-01-06", lunar.getSolar().toString())

    def test18(self):
        lunar = Lunar.fromYmd(2021, 12, 29)
        self.assertEqual("除夕", lunar.getFestivals()[0])

    def test19(self):
        lunar = Lunar.fromYmd(2020, 12, 30)
        self.assertEqual("除夕", lunar.getFestivals()[0])

    def test20(self):
        lunar = Lunar.fromYmd(2020, 12, 29)
        self.assertEqual(0, len(lunar.getFestivals()))

    def test21(self):
        solar = Solar.fromYmd(2022, 1, 31)
        lunar = solar.getLunar()
        self.assertEqual("除夕", lunar.getFestivals()[0])

    def testNext(self):
        solar = Solar.fromYmdHms(2020, 1, 10, 12, 0, 0)
        lunar = solar.getLunar()
        for i in range(-1, 1):
            self.assertEqual(solar.next(i).getLunar().toFullString(), lunar.next(i).toFullString())
