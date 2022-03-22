# -*- coding: utf-8 -*-
from datetime import timedelta
from math import ceil

from . import ExactDate, Solar
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
        return "%d.%d.%d" % (self.__year, self.__month, self.getIndex())

    def toFullString(self):
        return "%d年%d月第%d周" % (self.__year, self.__month, self.getIndex())

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        获取当前日期是在当月第几周
        :return: 周序号，从1开始
        """
        first_day = ExactDate.fromYmd(self.__year, self.__month, 1)
        first_day_week = first_day.isoweekday()
        if 7 == first_day_week:
            first_day_week = 0
        offset = first_day_week - self.__start
        if offset < 0:
            offset += 7
        return int(ceil((self.__day + offset) * 1.0 / 7))

    def getIndexInYear(self):
        """
        获取当前日期是在当年第几周
        :return: 周序号，从1开始
        """
        first_day = ExactDate.fromYmd(self.__year, 1, 1)
        first_day_week = first_day.isoweekday()
        if 7 == first_day_week:
            first_day_week = 0
        offset = first_day_week - self.__start
        if offset < 0:
            offset += 7
        return int(ceil((SolarUtil.getDaysInYear(self.__year, self.__month, self.__day) + offset) * 1.0 / 7))

    def getFirstDay(self):
        """
        获取本周第一天的阳历日期（可能跨月）
        :return: 本周第一天的阳历日期
        """
        date = ExactDate.fromYmd(self.__year, self.__month, self.__day)
        week = date.isoweekday()
        if week == 7:
            week = 0
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
        for day in self.getDays():
            if self.__month == day.getMonth():
                return day
        return None

    def getDays(self):
        """
        获取本周的阳历日期列表（可能跨月）
        :return: 本周的阳历日期列表
        """
        days = []
        first = self.getFirstDay()
        days.append(first)
        for i in range(1, 7):
            days.append(first.next(i))
        return days

    def getDaysInMonth(self):
        """
        获取本周的阳历日期列表（仅限当月）
        :return: 本周的阳历日期列表（仅限当月）
        """
        days = []
        for day in self.getDays():
            if self.__month == day.getMonth():
                days.append(day)
        return days

    def next(self, weeks, separate_month):
        """
        周推移
        :param weeks: 推移的周数，负数为倒推
        :param separate_month: 是否按月单独计算
        :return: 推移后的阳历周
        """
        if 0 == weeks:
            return SolarWeek.fromYmd(self.__year, self.__month, self.__day, self.__start)
        if separate_month:
            n = weeks
            c = ExactDate.fromYmd(self.__year, self.__month, self.__day)
            week = SolarWeek.fromDate(c, self.__start)
            month = self.__month
            plus = n > 0
            days = 7 if plus else -7
            while 0 != n:
                c = c + timedelta(days=days)
                week = SolarWeek.fromDate(c, self.__start)
                week_month = week.getMonth()
                if month != week_month:
                    index = week.getIndex()
                    if plus:
                        if 1 == index:
                            first_day = week.getFirstDay()
                            week = SolarWeek.fromYmd(first_day.getYear(), first_day.getMonth(), first_day.getDay(), self.__start)
                            week_month = week.getMonth()
                        else:
                            c = ExactDate.fromYmd(week.getYear(), week.getMonth(), 1)
                            week = SolarWeek.fromDate(c, self.__start)
                    else:
                        size = SolarUtil.getWeeksOfMonth(week.getYear(), week.getMonth(), self.__start)
                        if size == index:
                            first_day = week.getFirstDay()
                            last_day = first_day.next(6)
                            week = SolarWeek.fromYmd(last_day.getYear(), last_day.getMonth(), last_day.getDay(), self.__start)
                            week_month = week.getMonth()
                        else:
                            c = ExactDate.fromYmd(week.getYear(), week.getMonth(), SolarUtil.getDaysOfMonth(week.getYear(), week.getMonth()))
                            week = SolarWeek.fromDate(c, self.__start)
                    month = week_month
                n -= 1 if plus else -1
            return week
        else:
            c = ExactDate.fromYmd(self.__year, self.__month, self.__day)
            c = c + timedelta(days=weeks * 7)
            return SolarWeek.fromDate(c, self.__start)
