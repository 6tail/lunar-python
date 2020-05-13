# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from math import ceil, floor
from .util import SolarUtil


class Solar:
    """
    阳历日期
    """

    # 2000年儒略日数(2000-1-1 12:00:00 UTC)
    J2000 = 2451545

    def __init__(self, year, month, day, hour, minute, second):
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__calendar = datetime(year, month, day, hour, minute, second)

    @staticmethod
    def __int2(v):
        v = int(floor(v))
        return v + 1 if v < 0 else v

    @staticmethod
    def fromDate(date):
        return Solar(date.year, date.month, date.day, date.hour, date.minute, date.second)

    @staticmethod
    def fromJulianDay(julianDay):
        julianDay += 0.5
        # 日数的整数部份
        a = Solar.__int2(julianDay)
        # 日数的小数部分
        f = julianDay - a
        if a > 2299161:
            dd = Solar.__int2((a - 1867216.25) / 36524.25)
            a += 1 + dd - Solar.__int2(dd / 4)
        # 向前移4年零2个月
        a += 1524
        y = Solar.__int2((a - 122.1) / 365.25)
        # 去除整年日数后余下日数
        dd = a - Solar.__int2(365.25 * y)
        m = int(Solar.__int2(dd / 30.6001))
        # 去除整月日数后余下日数
        d = int(Solar.__int2(dd - Solar.__int2(m * 30.6001)))
        y -= 4716
        m -= 1
        if m > 12:
            m -= 12
        if m <= 2:
            y += 1
        # 日的小数转为时分秒
        f *= 24
        h = int(Solar.__int2(f))

        f -= h
        f *= 60
        mi = Solar.__int2(f)

        f -= mi
        f *= 60
        s = Solar.__int2(f)
        return Solar(y, m, d, h, mi, s)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmd(year, month, day):
        return Solar(year, month, day, 0, 0, 0)

    def isLeapYear(self):
        """
        是否闰年
        :return: True/False 闰年/非闰年
        """
        return SolarUtil.isLeapYear(self.__year)

    def getWeek(self):
        """
        获取星期，0代表周日，1代表周一
        :return: 0123456
        """
        return int(self.__calendar.strftime("%w"))

    def getWeekInChinese(self):
        """
        获取星期的中文
        :return: 日一二三四五六
        """
        return SolarUtil.WEEK[self.getWeek()]

    def getFestivals(self):
        """
        获取节日，有可能一天会有多个节日
        :return: 劳动节等
        """
        l = []
        md = str(self.__month) + "-" + str(self.__day)
        if md in SolarUtil.FESTIVAL:
            l.append(SolarUtil.FESTIVAL[md])
        week = self.getWeek()
        weekInMonth = int(ceil((self.__day - week) / 7))
        if week > 0:
            weekInMonth += 1
        me = str(self.__month) + "-" + str(weekInMonth) + "-" + str(week)
        if me in SolarUtil.WEEK_FESTIVAL:
            l.append(SolarUtil.WEEK_FESTIVAL[me])
        return l

    def getOtherFestivals(self):
        """
        获取非正式的节日，有可能一天会有多个节日
        :return: 非正式的节日列表，如中元节
        """
        l = []
        md = str(self.__month) + "-" + str(self.__day)
        if md in SolarUtil.OTHER_FESTIVAL:
            fs = SolarUtil.OTHER_FESTIVAL[md]
            for f in fs:
                l.append(f)
        return l

    def getXingZuo(self):
        """
        获取星座
        :return: 星座
        """
        index = 11
        m = self.__month
        d = self.__day
        y = m * 100 + d
        if 321 <= y <= 419:
            index = 0
        elif 420 <= y <= 520:
            index = 1
        elif 521 <= y <= 620:
            index = 2
        elif 621 <= y <= 722:
            index = 3
        elif 723 <= y <= 822:
            index = 4
        elif 823 <= y <= 922:
            index = 5
        elif 923 <= y <= 1022:
            index = 6
        elif 1023 <= y <= 1121:
            index = 7
        elif 1122 <= y <= 1221:
            index = 8
        elif y >= 1222 or y <= 119:
            index = 9
        elif y <= 218:
            index = 10
        return SolarUtil.XING_ZUO[index]

    def getJulianDay(self):
        """
        获取儒略日
        :return: 儒略日
        """
        y = self.__year
        m = self.__month
        n = 0

        if m <= 2:
            m += 12
            y -= 1

        # 判断是否为UTC日1582 * 372 + 10 * 31 + 15
        if self.__year * 372 + self.__month * 31 + self.__day >= 588829:
            n = Solar.__int2(y / 100)
            # 加百年闰
            n = 2 - n + Solar.__int2(n / 4)

        # 加上年引起的偏移日数
        n += Solar.__int2(365.2500001 * (y + 4716))
        # 加上月引起的偏移日数及日偏移数
        n += Solar.__int2(30.6 * (m + 1)) + self.__day
        n += ((self.__second * 1.0 / 60 + self.__minute) / 60 + self.__hour) / 24 - 1524.5
        return n

    def getLunar(self):
        """
        获取农历
        :return: 农历
        """
        from lunar_python import Lunar
        return Lunar.fromDate(self.__calendar)

    def next(self, days):
        """
        获取往后推几天的阳历日期，如果要往前推，则天数用负数
        :param days: 天数
        :return: 阳历日期
        """
        c = datetime(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)
        c = c + timedelta(days=days)
        return Solar.fromDate(c)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

    def getHour(self):
        return self.__hour

    def getMinute(self):
        return self.__minute

    def getSecond(self):
        return self.__second

    def getCalendar(self):
        return self.__calendar

    def toYmd(self):
        return str(self.__year) + "-" + ("0" if self.__month < 10 else "") + str(self.__month) + "-" + ("0" if self.__day < 10 else "") + str(self.__day)

    def toYmdHms(self):
        return self.toYmd() + " " + ("0" if self.__hour < 10 else "") + str(self.__hour) + ":" + ("0" if self.__minute < 10 else "") + str(self.__minute) + ":" + ("0" if self.__second < 10 else "") + str(self.__second)

    def toFullString(self):
        s = self.toYmdHms()
        if self.isLeapYear():
            s += " 闰年"
        s += " 星期"
        s += self.getWeekInChinese()
        for f in self.getFestivals():
            s += " (" + f + ")"
        for f in self.getOtherFestivals():
            s += " (" + f + ")"
        s += " "
        s += self.getXingZuo()
        s += "座"
        return s

    def toString(self):
        return self.toYmd()

    def __str__(self):
        return self.toString()
