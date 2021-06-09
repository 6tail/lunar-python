# -*- coding: utf-8 -*-
from math import ceil

from . import SolarMonth


class SolarHalfYear:
    """
    阳历半年
    """

    MONTH_COUNT = 6

    def __init__(self, year, month):
        self.__year = year
        self.__month = month

    @staticmethod
    def fromDate(date):
        return SolarHalfYear(date.year, date.month)

    @staticmethod
    def fromYm(year, month):
        return SolarHalfYear(year, month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def toString(self):
        return "%d.%d" % (self.__year, self.getIndex())

    def toFullString(self):
        return "%d年%s半年" % (self.__year, ("上" if 1 == self.getIndex() else "下"))

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        获取当月是第几半年
        :return: 半年序号，从1开始
        """
        return int(ceil(self.__month * 1.0 / SolarHalfYear.MONTH_COUNT))

    def getMonths(self):
        """
        获取本半年的阳历月列表
        :return: 阳历月列表
        """
        months = []
        index = self.getIndex() - 1
        for i in range(0, SolarHalfYear.MONTH_COUNT):
            months.append(SolarMonth.fromYm(self.__year, SolarHalfYear.MONTH_COUNT * index + i + 1))
        return months

    def next(self, half_years):
        """
        半年推移
        :param half_years: 推移的半年数，负数为倒推
        :return: 推移后的半年
        """
        if 0 == half_years:
            return SolarHalfYear.fromYm(self.__year, self.__month)
        year = self.__year
        month = self.__month
        months = SolarHalfYear.MONTH_COUNT * half_years
        if months == 0:
            return SolarMonth.fromYm(year, month)
        n = abs(months)
        for i in range(1, n + 1):
            if months < 0:
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
            else:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
        return SolarHalfYear.fromYm(year, month)
