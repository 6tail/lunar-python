# -*- coding: utf-8 -*-
import unittest
from lunar_python import Lunar, Solar


class LunarTest(unittest.TestCase):

    def test(self):
        date = Lunar.fromYmdHms(2019, 3, 27, 0, 0, 0)
        self.assertEqual("二〇一九年三月廿七", date.toString())
        self.assertEqual("二〇一九年三月廿七 己亥(猪)年 戊辰(龙)月 戊戌(狗)日 子(鼠)时 纳音[平地木 大林木 平地木 桑柘木] 星期三 西方白虎 星宿[参水猿](吉) 彭祖百忌[戊不受田田主不祥 戌不吃犬作怪上床] 喜神方位[巽](东南) 阳贵神方位[艮](东北) 阴贵神方位[坤](西南) 福神方位[艮](东北) 财神方位[坎](正北) 冲[(壬辰)龙] 煞[北]", date.toFullString())
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
        lunar = Lunar.fromYmdHms(9997, 12, 21, 12, 0, 0)
        self.assertEqual("9998-01-11", lunar.getSolar().toString())

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

    def test22(self):
        lunar = Lunar.fromYmd(2033, -11, 1)
        self.assertEqual('2033-12-22', lunar.getSolar().toYmd())

    def test25(self):
        solar = Solar.fromYmdHms(2021, 6, 7, 21, 18, 0)
        self.assertEqual('二〇二一年四月廿七', solar.getLunar().toString())

    def test26(self):
        lunar = Lunar.fromYmdHms(2021, 6, 7, 21, 18, 0)
        self.assertEqual('2021-07-16', lunar.getSolar().toString())

    def testNext(self):
        solar = Solar.fromYmdHms(2020, 1, 10, 12, 0, 0)
        lunar = solar.getLunar()
        for i in range(-1, 1):
            self.assertEqual(solar.next(i).getLunar().toFullString(), lunar.next(i).toFullString())

    def test27(self):
        solar = Solar.fromYmd(1989, 4, 28)
        self.assertEqual(23, solar.getLunar().getDay())

    def test28(self):
        solar = Solar.fromYmd(1990, 10, 8)
        self.assertEqual("乙酉", solar.getLunar().getMonthInGanZhiExact())

    def test29(self):
        solar = Solar.fromYmd(1990, 10, 9)
        self.assertEqual("丙戌", solar.getLunar().getMonthInGanZhiExact())

    def test30(self):
        solar = Solar.fromYmd(1990, 10, 8)
        self.assertEqual("丙戌", solar.getLunar().getMonthInGanZhi())

    def test31(self):
        solar = Solar.fromYmdHms(1987, 4, 17, 9, 0, 0)
        self.assertEqual("一九八七年三月二十", solar.getLunar().toString())

    def test32(self):
        lunar = Lunar.fromYmd(2034, 1, 1)
        self.assertEqual("2034-02-19", lunar.getSolar().toYmd())

    def test33(self):
        lunar = Lunar.fromYmd(2033, 12, 1)
        self.assertEqual("2034-01-20", lunar.getSolar().toYmd())

    def test34(self):
        lunar = Lunar.fromYmd(37, -12, 1)
        self.assertEqual("闰腊", lunar.getMonthInChinese())

    def test36(self):
        solar = Solar.fromYmd(5553, 1, 22)
        self.assertEqual("五五五二年闰腊月初二", solar.getLunar().toString())

    def test37(self):
        solar = Solar.fromYmd(7013, 12, 24)
        self.assertEqual("七〇一三年闰冬月初四", solar.getLunar().toString())

    def test38(self):
        lunar = Lunar.fromYmd(7013, -11, 4)
        self.assertEqual("7013-12-24", lunar.getSolar().toString())

    def test39(self):
        solar = Solar.fromYmd(1987, 4, 12)
        lunar = solar.getLunar()
        self.assertEqual("一九八七年三月十五", lunar.toString())

    def test40(self):
        solar = Solar.fromYmd(1987, 4, 13)
        lunar = solar.getLunar()
        self.assertEqual("一九八七年三月十六", lunar.toString())

    def test41(self):
        solar = Solar.fromYmd(4, 2, 10)
        lunar = solar.getLunar()
        self.assertEqual("鼠", lunar.getYearShengXiao())

    def test42(self):
        solar = Solar.fromYmd(4, 2, 9)
        lunar = solar.getLunar()
        self.assertEqual("猪", lunar.getYearShengXiao())

    def test43(self):
        solar = Solar.fromYmd(2017, 2, 15)
        lunar = solar.getLunar()
        self.assertEqual("子命互禄 辛命进禄", lunar.getDayLu())

    def test44(self):
        solar = Solar.fromYmd(2017, 2, 16)
        lunar = solar.getLunar()
        self.assertEqual("寅命互禄", lunar.getDayLu())

    def test48(self):
        solar = Solar.fromYmd(2021, 11, 13)
        lunar = solar.getLunar()
        self.assertEqual("碓磨厕 外东南", lunar.getDayPositionTai())

    def test49(self):
        solar = Solar.fromYmd(2021, 11, 12)
        lunar = solar.getLunar()
        self.assertEqual("占门碓 外东南", lunar.getDayPositionTai())

    def test50(self):
        solar = Solar.fromYmd(2021, 11, 13)
        lunar = solar.getLunar()
        self.assertEqual("西南", lunar.getDayPositionFuDesc())

    def test51(self):
        solar = Solar.fromYmd(2021, 11, 12)
        lunar = solar.getLunar()
        self.assertEqual("正北", lunar.getDayPositionFuDesc())

    def test52(self):
        solar = Solar.fromYmd(2011, 11, 12)
        lunar = solar.getLunar()
        self.assertEqual("厨灶厕 外西南", lunar.getDayPositionTai())

    def test53(self):
        solar = Solar.fromYmd(1722, 9, 25)
        lunar = solar.getLunar()
        self.assertEqual("秋社", lunar.getOtherFestivals()[0])

    def test54(self):
        solar = Solar.fromYmd(840, 9, 14)
        lunar = solar.getLunar()
        self.assertEqual("秋社", lunar.getOtherFestivals()[0])

    def test55(self):
        solar = Solar.fromYmd(2022, 3, 16)
        lunar = solar.getLunar()
        self.assertEqual("春社", lunar.getOtherFestivals()[0])

    def test56(self):
        solar = Solar.fromYmd(2021, 3, 21)
        lunar = solar.getLunar()
        self.assertEqual("春社", lunar.getOtherFestivals()[0])

    def test57(self):
        self.assertEqual("1582-10-04", Lunar.fromYmd(1582, 9, 18).getSolar().toYmd())

    def test58(self):
        self.assertEqual("1582-10-15", Lunar.fromYmd(1582, 9, 19).getSolar().toYmd())

    def test59(self):
        self.assertEqual("1518-02-10", Lunar.fromYmd(1518, 1, 1).getSolar().toYmd())

    def test60(self):
        self.assertEqual("0793-02-15", Lunar.fromYmd(793, 1, 1).getSolar().toYmd())

    def test61(self):
        self.assertEqual("2025-07-25", Lunar.fromYmd(2025, -6, 1).getSolar().toYmd())

    def test62(self):
        self.assertEqual("2025-06-25", Lunar.fromYmd(2025, 6, 1).getSolar().toYmd())

    def test63(self):
        self.assertEqual("0193-02-19", Lunar.fromYmd(193, 1, 1).getSolar().toYmd())

    def test64(self):
        self.assertEqual("0041-02-20", Lunar.fromYmd(41, 1, 1).getSolar().toYmd())

    def test65(self):
        self.assertEqual("0554-02-18", Lunar.fromYmd(554, 1, 1).getSolar().toYmd())

    def test66(self):
        self.assertEqual("1070-02-14", Lunar.fromYmd(1070, 1, 1).getSolar().toYmd())

    def test67(self):
        self.assertEqual("1537-02-10", Lunar.fromYmd(1537, 1, 1).getSolar().toYmd())

    def test68(self):
        self.assertEqual("九一七年闰十月十四", Solar.fromYmd(917, 12, 1).getLunar().toString())

    def test69(self):
        self.assertEqual("九一七年冬月十五", Solar.fromYmd(917, 12, 31).getLunar().toString())

    def test70(self):
        self.assertEqual("九一七年冬月十六", Solar.fromYmd(918, 1, 1).getLunar().toString())
