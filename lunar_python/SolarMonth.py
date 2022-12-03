# -*- coding: utf-8 -*-

from . import Solar, SolarWeek
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
        return "%d-%d" % (self.__year, self.__month)

    def toFullString(self):
        return "%d年%d月" % (self.__year, self.__month)

    def __str__(self):
        return self.toString()

    def getDays(self):
        """
        获取本月的阳历日期列表
        :return: 阳历日期列表
        """
        days = []
        d = Solar.fromYmd(self.__year, self.__month, 1)
        days.append(d)
        for i in range(1, SolarUtil.getDaysOfMonth(self.__year, self.__month)):
            days.append(d.next(i))
        return days

    def getWeeks(self, start):
        """
        获取本月的阳历日期列表
        :param start: 星期几作为一周的开始，1234560分别代表星期一至星期天
        :return: 阳历日期列表
        """
        weeks = []
        week = SolarWeek.fromYmd(self.__year, self.__month, 1, start)
        while True:
            weeks.append(week)
            week = week.next(1, False)
            first_day = week.getFirstDay()
            if first_day.getYear() > self.__year or first_day.getMonth() > self.__month:
                break
        return weeks

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
