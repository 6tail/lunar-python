# -*- coding: utf-8 -*-
from . import Solar, LunarYear, NineStar
from .util import LunarUtil


class LunarMonth:
    """
    农历月
    """

    def __init__(self, lunar_year, lunar_month, day_count, first_julian_day):
        self.__year = lunar_year
        self.__month = lunar_month
        self.__dayCount = day_count
        self.__firstJulianDay = first_julian_day

    @staticmethod
    def fromYm(lunar_year, lunar_month):
        from . import LunarYear
        return LunarYear.fromYear(lunar_year).getMonth(lunar_month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def isLeap(self):
        return self.__month < 0

    def getDayCount(self):
        return self.__dayCount

    def getFirstJulianDay(self):
        return self.__firstJulianDay

    def getPositionTaiSui(self):
        m = abs(self.__month) % 4
        if 0 == m:
            p = "巽"
        elif 1 == m:
            p = "艮"
        elif 3 == m:
            p = "坤"
        else:
            p = LunarUtil.POSITION_GAN[Solar.fromJulianDay(self.getFirstJulianDay()).getLunar().getMonthGanIndex()]
        return p

    def getPositionTaiSuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionTaiSui()]

    def getNineStar(self):
        index = LunarYear.fromYear(self.__year).getZhiIndex() % 3
        m = abs(self.__month)
        month_zhi_index = (13 + m) % 12
        n = 27 - (index * 3)
        if month_zhi_index < LunarUtil.BASE_MONTH_ZHI_INDEX:
            n -= 3
        offset = (n - month_zhi_index) % 9
        return NineStar.fromIndex(offset)

    def toString(self):
        return "%d年%s%s月(%d天)" % (self.__year, ("闰" if self.isLeap() else ""), LunarUtil.MONTH[abs(self.__month)], self.__dayCount)

    def __str__(self):
        return self.toString()
