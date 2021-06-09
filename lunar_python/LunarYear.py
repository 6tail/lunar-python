# -*- coding: utf-8 -*-
from .util import ShouXingUtil


class LunarYear:
    """
    农历年
    """

    def __init__(self, lunar_year):
        self.__year = lunar_year
        self.__months = []
        self.__jieQiJulianDays = []
        self.compute()

    @staticmethod
    def fromYear(year):
        return LunarYear(year)

    def compute(self):
        from . import Lunar, Solar, LunarMonth
        # 节气(中午12点)，长度25
        jq = []
        # 合朔，即每月初一(中午12点)，长度16
        hs = []
        # 每月天数，长度15
        day_counts = []
        year = self.__year - 2000
        # 从上年的大雪到下年的立春
        for i in range(0, len(Lunar.JIE_QI_IN_USE)):
            # 精确的节气
            t = 36525 * ShouXingUtil.saLonT((year + (17 + i) * 15.0 / 360) * ShouXingUtil.PI_2)
            t += ShouXingUtil.ONE_THIRD - ShouXingUtil.dtT(t)
            self.__jieQiJulianDays.append(t + Solar.J2000)
            # 按中午12点算的节气
            if 0 < i < 26:
                jq.append(round(t))
        # 冬至前的初一
        w = ShouXingUtil.calcShuo(jq[0])
        if w > jq[0]:
            w -= 29.5306
        # 递推每月初一
        for i in range(0, 16):
            hs.append(ShouXingUtil.calcShuo(w + 29.5306 * i))
        # 每月天数
        for i in range(0, 15):
            day_counts.append(int(hs[i + 1] - hs[i]))

        leap = -1
        if hs[13] <= jq[24]:
            i = 1
            while hs[i + 1] > jq[2 * i] and i < 13:
                i += 1
            leap = i
        y = self.__year - 1
        m = 11
        for i in range(0, 15):
            is_leap = False
            if i == leap:
                is_leap = True
                m -= 1
            self.__months.append(LunarMonth(y, -m if is_leap else m, day_counts[i], hs[i] + Solar.J2000))
            m += 1
            if m == 13:
                m = 1
                y += 1

    def getYear(self):
        return self.__year

    def toString(self):
        return str(self.__year) + ""

    def toFullString(self):
        return "%d年" % self.__year

    def __str__(self):
        return self.toString()

    def getMonths(self):
        return self.__months

    def getJieQiJulianDays(self):
        return self.__jieQiJulianDays

    def getLeapMonth(self):
        """
        获取闰月
        :return: 闰月数字，1代表闰1月，0代表无闰月
        """
        for i in range(0, len(self.__months)):
            m = self.__months[i]
            if m.getYear() == self.__year and m.isLeap():
                return abs(m.getMonth())
        return 0

    def getMonth(self, lunar_month):
        """
        获取农历月
        :param lunar_month: 闰月数字，1代表闰1月，0代表无闰月
        :return: 农历月
        """
        for i in range(0, len(self.__months)):
            m = self.__months[i]
            if m.getYear() == self.__year and m.getMonth() == lunar_month:
                return m
        return None
