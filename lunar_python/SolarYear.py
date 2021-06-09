# -*- coding: utf-8 -*-

from . import SolarMonth


class SolarYear:
    """
    阳历年
    """

    MONTH_COUNT = 12

    def __init__(self, year):
        self.__year = year

    @staticmethod
    def fromDate(date):
        return SolarYear(date.year)

    @staticmethod
    def fromYear(year):
        return SolarYear(year)

    def getYear(self):
        return self.__year

    def toString(self):
        return str(self.__year)

    def toFullString(self):
        return "%d年" % self.__year

    def __str__(self):
        return self.toString()

    def getMonths(self):
        """
        获取本年的阳历月列表
        :return: 阳历月列表
        """
        months = []
        m = SolarMonth.fromYm(self.__year, 1)
        months.append(m)
        for i in range(1, SolarYear.MONTH_COUNT):
            months.append(m.next(i))
        return months

    def next(self, years):
        """
        获取往后推几年的阳历年，如果要往前推，则月数用负数
        :param years: 年数
        :return: 阳历年
        """
        return SolarYear.fromYear(self.__year + years)
