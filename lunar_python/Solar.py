# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from math import ceil
from .util import SolarUtil, LunarUtil, HolidayUtil


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
    def fromDate(date):
        return Solar(date.year, date.month, date.day, date.hour, date.minute, date.second)

    @staticmethod
    def fromJulianDay(julianDay):
        d = int(julianDay + 0.5)
        f = julianDay + 0.5 - d
        if d >= 2299161:
            c = int((d - 1867216.25) / 36524.25)
            d += 1 + c - int(c / 4)
        d += 1524
        year = int((d - 122.1) / 365.25)
        d -= int(365.25 * year)
        month = int(d / 30.601)
        d -= int(30.601 * month)
        day = d
        if month > 13:
            month -= 13
            year -= 4715
        else:
            month -= 1
            year -= 4716
        f *= 24
        hour = int(f)

        f -= hour
        f *= 60
        minute = int(f)

        f -= minute
        f *= 60
        second = int(round(f))
        if second == 60:
            second = 59
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmd(year, month, day):
        return Solar(year, month, day, 0, 0, 0)

    @staticmethod
    def fromBaZi(yearGanZhi, monthGanZhi, dayGanZhi, timeGanZhi):
        l = []
        today = Solar.fromDate(datetime.now())
        lunar = today.getLunar()
        offsetYear = LunarUtil.getJiaZiIndex(lunar.getYearInGanZhiExact()) - LunarUtil.getJiaZiIndex(yearGanZhi)
        if offsetYear < 0:
            offsetYear = offsetYear + 60
        startYear = today.getYear() - offsetYear
        hour = 0
        timeZhi = timeGanZhi[len(timeGanZhi) / 2:]
        for i in range(0, len(LunarUtil.ZHI)):
            if LunarUtil.ZHI[i] == timeZhi:
                hour = (i - 1) * 2
        while startYear >= SolarUtil.BASE_YEAR - 1:
            year = startYear - 1
            counter = 0
            month = 12
            found = False
            while counter < 15:
                if year >= SolarUtil.BASE_YEAR:
                    day = 1
                    if year == SolarUtil.BASE_YEAR and month == SolarUtil.BASE_MONTH:
                        day = SolarUtil.BASE_DAY
                    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
                    lunar = solar.getLunar()
                    if lunar.getYearInGanZhiExact() == yearGanZhi and lunar.getMonthInGanZhiExact() == monthGanZhi:
                        found = True
                        break
                month += 1
                if month > 12:
                    month = 1
                    year += 1
                counter += 1
            if found:
                counter = 0
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
                day = 1
                if year == SolarUtil.BASE_YEAR and month == SolarUtil.BASE_MONTH:
                    day = SolarUtil.BASE_DAY
                solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
                while counter < 61:
                    lunar = solar.getLunar()
                    if lunar.getYearInGanZhiExact() == yearGanZhi and lunar.getMonthInGanZhiExact() == monthGanZhi and lunar.getDayInGanZhiExact() == dayGanZhi and lunar.getTimeInGanZhi() == timeGanZhi:
                        l.append(solar)
                        break
                    solar = solar.next(1)
                    counter += 1
            startYear -= 60
        return l

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
        d = self.__day + ((self.__second / 60 + self.__minute) / 60 + self.__hour) / 24
        n = 0
        g = False
        if y * 372 + m * 31 + int(d) >= 588829:
            g = True
        if m <= 2:
            m += 12
            y -= 1
        if g:
            n = int(y / 100)
            n = 2 - n + int(n / 4)
        return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + n - 1524.5

    def getLunar(self):
        """
        获取农历
        :return: 农历
        """
        from .Lunar import Lunar
        return Lunar.fromDate(self.__calendar)

    def next(self, days):
        """
        获取往后推几天的阳历日期，如果要往前推，则天数用负数
        :param days: 天数
        :return: 阳历日期
        """
        c = datetime(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)
        if days != 0:
            c = c + timedelta(days=days)
        return Solar.fromDate(c)

    def nextWorkday(self, days):
        """
        获取往后推几个工作日的阳历日期，如果要往前推，则天数用负数
        :param days: 天数
        :return: 阳历日期
        """
        c = datetime(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)
        if days != 0:
            rest = abs(days)
            add = 1
            if days < 1:
                add = -1
            while rest > 0:
                c = c + timedelta(days=add)
                work = True
                holiday = HolidayUtil.getHoliday(c.year, c.month, c.day)
                if holiday is None:
                    week = int(c.strftime("%w"))
                    if week == 0 or week == 6:
                        work = False
                else:
                    work = holiday.isWork()
                if work:
                    rest -= 1
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
