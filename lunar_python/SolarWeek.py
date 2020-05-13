# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from math import ceil

from .Solar import Solar
from .util import SolarUtil


class SolarWeek:
    """
    阳历周
    """

    def __init__(self, year, month, day, start):
        """
        通过年月日初始化
        :param year: 年
        :param month: 月，1到12
        :param day: 日，1到31
        :param start: 星期几作为一周的开始，1234560分别代表星期一至星期天
        """
        self.__year = year
        self.__month = month
        self.__day = day
        self.__start = start

    @staticmethod
    def fromDate(date, start):
        return SolarWeek(date.year, date.month, date.day, start)

    @staticmethod
    def fromYmd(year, month, day, start):
        return SolarWeek(year, month, day, start)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

    def getStart(self):
        return self.__start

    def toString(self):
        return str(self.__year) + "." + str(self.__month) + "." + str(self.getIndex())

    def toFullString(self):
        return str(self.__year) + "年" + str(self.__month) + "月第" + str(self.getIndex()) + "周"

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        获取当前日期是在当月第几周
        :return: 周序号，从1开始
        """
        firstDay = datetime(self.__year, self.__month, 1)
        firstDayWeek = int(firstDay.strftime("%w"))
        if firstDayWeek == 0:
            firstDayWeek = 7
        return int(ceil((self.__day + firstDayWeek - self.__start) * 1.0 / 7))

    def getFirstDay(self):
        """
        获取本周第一天的阳历日期（可能跨月）
        :return: 本周第一天的阳历日期
        """
        date = datetime(self.__year, self.__month, self.__day)
        week = int(date.strftime("%w"))
        prev = week - self.__start
        if prev < 0:
            prev += 7
        date = date + timedelta(days=-prev)
        return Solar.fromDate(date)

    def getFirstDayInMonth(self):
        """
        获取本周第一天的阳历日期（仅限当月）
        :return: 本周第一天的阳历日期
        """
        days = self.getDays()
        for day in days:
            if self.__month == day.getMonth():
                return day
        return None

    def getDays(self):
        """
        获取本周的阳历日期列表（可能跨月）
        :return: 本周的阳历日期列表
        """
        l = []
        first = self.getFirstDay()
        l.append(first)
        for i in range(1, 7):
            l.append(first.next(i))
        return l

    def getDaysInMonth(self):
        """
        获取本周的阳历日期列表（仅限当月）
        :return: 本周的阳历日期列表（仅限当月）
        """
        l = []
        days = self.getDays()
        for day in days:
            if self.__month == day.getMonth():
                l.append(days)
        return l

    def next(self, weeks, separateMonth):
        """
        周推移
        :param weeks: 推移的周数，负数为倒推
        :param separateMonth: 是否按月单独计算
        :return: 推移后的阳历周
        """
        if 0 == weeks:
            return SolarWeek.fromYmd(self.__year, self.__month, self.__day, self.__start)
        if separateMonth:
            n = weeks
            c = datetime(self.__year, self.__month, self.__day)
            week = SolarWeek.fromDate(c, self.__start)
            month = self.__month
            plus = n > 0
            days = 7 if plus else -7
            while 0 != n:
                c = c + timedelta(days=days)
                week = SolarWeek.fromDate(c, self.__start)
                weekMonth = week.getMonth()
                if month != weekMonth:
                    index = week.getIndex()
                    if plus:
                        if 1 == index:
                            firstDay = week.getFirstDay()
                            week = SolarWeek.fromYmd(firstDay.getYear(), firstDay.getMonth(), firstDay.getDay(), self.__start)
                            weekMonth = week.getMonth()
                        else:
                            c = datetime(week.getYear(), week.getMonth(), 1)
                            week = SolarWeek.fromDate(c, self.__start)
                    else:
                        size = SolarUtil.getWeeksOfMonth(week.getYear(), week.getMonth(), self.__start)
                        if size == index:
                            firstDay = week.getFirstDay()
                            lastDay = firstDay.next(6)
                            week = SolarWeek.fromYmd(lastDay.getYear(), lastDay.getMonth(), lastDay.getDay(), self.__start)
                            weekMonth = week.getMonth()
                        else:
                            c = datetime(week.getYear(), week.getMonth(), SolarUtil.getDaysOfMonth(week.getYear(), week.getMonth()))
                            week = SolarWeek.fromDate(c, self.__start)
                    month = weekMonth
                n -= 1 if plus else -1
            return week
        else:
            c = datetime(self.__year, self.__month, self.__day)
            c = c + timedelta(days=weeks * 7)
            return SolarWeek.fromDate(c, self.__start)
