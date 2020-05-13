# -*- coding: utf-8 -*-
from math import ceil

from .SolarMonth import SolarMonth


class SolarSeason:
    """
    阳历季度
    """

    MONTH_COUNT = 3

    def __init__(self, year, month):
        self.__year = year
        self.__month = month

    @staticmethod
    def fromDate(date):
        return SolarSeason(date.year, date.month)

    @staticmethod
    def fromYm(year, month):
        return SolarSeason(year, month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def toString(self):
        return str(self.__year) + "." + str(self.getIndex())

    def toFullString(self):
        return str(self.__year) + "年" + str(self.getIndex()) + "季度"

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        获取当月是第几季度
        :return: 季度序号，从1开始
        """
        return int(ceil(self.__month * 1.0 / SolarSeason.MONTH_COUNT))

    def getMonths(self):
        """
        获取本季度的阳历月列表
        :return: 阳历月列表
        """
        l = []
        index = self.getIndex() - 1
        for i in range(0, SolarSeason.MONTH_COUNT):
            l.append(SolarMonth.fromYm(self.__year, SolarSeason.MONTH_COUNT * index + i + 1))
        return l

    def next(self, seasons):
        """
        季度推移
        :param seasons: 推移的季度数，负数为倒推
        :return: 推移后的季度
        """
        if 0 == seasons:
            return SolarSeason.fromYm(self.__year, self.__month)
        year = self.__year
        month = self.__month
        months = SolarSeason.MONTH_COUNT * seasons
        if months == 0:
            return SolarSeason.fromYm(year, month)
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
        return SolarSeason.fromYm(year, month)
