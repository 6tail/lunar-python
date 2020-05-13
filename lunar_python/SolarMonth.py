# -*- coding: utf-8 -*-

from .Solar import Solar
from .util import SolarUtil


class SolarMonth:
    """
    阳历月
    """

    def __init__(self, year, month):
        self.__year = year
        self.__month = month

    @staticmethod
    def fromDate(date):
        return SolarMonth(date.year, date.month)

    @staticmethod
    def fromYm(year, month):
        return SolarMonth(year, month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def toString(self):
        return str(self.__year) + "-" + str(self.__month)

    def toFullString(self):
        return str(self.__year) + "年" + str(self.__month) + "月"

    def __str__(self):
        return self.toString()

    def getDays(self):
        """
        获取本月的阳历日期列表
        :return: 阳历日期列表
        """
        l = []
        d = Solar.fromYmd(self.__year, self.__month, 1)
        l.append(d)
        days = SolarUtil.getDaysOfMonth(self.__year, self.__month)
        for i in range(1, days):
            l.append(d.next(i))
        return l

    def next(self, months):
        """
        获取往后推几个月的阳历月，如果要往前推，则月数用负数
        :param months: 月数
        :return: 阳历月
        """
        year = self.__year
        month = self.__month
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
        return SolarMonth.fromYm(year, month)
