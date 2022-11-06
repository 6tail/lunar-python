# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from math import ceil

from . import ExactDate
from .util import SolarUtil, LunarUtil, HolidayUtil


class Solar:
    """
    阳历日期
    """

    # 2000年儒略日数(2000-1-1 12:00:00 UTC)
    J2000 = 2451545

    def __init__(self, year, month, day, hour, minute, second):
        ymd = "%04d-%02d-%02d" % (year, month, day)
        if year > 9999 or year < 1:
            raise Exception("not support solar %s" % ymd)
        if year == 1582 and month == 10:
            if day >= 15:
                day -= 10
        if month == 2:
            leap = SolarUtil.isLeapYear(year)
            if day > 28 and not leap:
                month += int(day / 28)
                day = day % 28
            if day > 29 and not leap:
                month += int(day / 29)
                day = day % 29
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__calendar = ExactDate.fromYmdHms(year, month, day, hour, minute, second)

    @staticmethod
    def fromDate(date):
        return Solar(date.year, date.month, date.day, date.hour, date.minute, date.second)

    @staticmethod
    def fromJulianDay(julian_day):
        d = int(julian_day + 0.5)
        f = julian_day + 0.5 - d
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
        if second > 59:
            second -= 60
            minute += 1
        if minute > 59:
            minute -= 60
            hour += 1
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmd(year, month, day):
        return Solar(year, month, day, 0, 0, 0)

    @staticmethod
    def fromBaZi(year_gan_zhi, month_gan_zhi, day_gan_zhi, time_gan_zhi, sect=2, base_year=1900):
        sect = 1 if 1 == sect else 2
        solar_list = []
        today = Solar.fromDate(datetime.now())
        lunar = today.getLunar()
        offset_year = LunarUtil.getJiaZiIndex(lunar.getYearInGanZhiExact()) - LunarUtil.getJiaZiIndex(year_gan_zhi)
        if offset_year < 0:
            offset_year = offset_year + 60
        start_year = lunar.getYear() - offset_year
        hour = 0
        time_zhi = time_gan_zhi[1:]
        for i in range(0, len(LunarUtil.ZHI)):
            if LunarUtil.ZHI[i] == time_zhi:
                hour = (i - 1) * 2
        while start_year >= base_year:
            year = start_year - 1
            counter = 0
            month = 12
            found = False
            while counter < 15:
                if year >= base_year:
                    day = 1
                    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
                    lunar = solar.getLunar()
                    if lunar.getYearInGanZhiExact() == year_gan_zhi and lunar.getMonthInGanZhiExact() == month_gan_zhi:
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
                solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
                while counter < 61:
                    lunar = solar.getLunar()
                    dgz = lunar.getDayInGanZhiExact2() if 2 == sect else lunar.getDayInGanZhiExact()
                    if lunar.getYearInGanZhiExact() == year_gan_zhi and lunar.getMonthInGanZhiExact() == month_gan_zhi and dgz == day_gan_zhi and lunar.getTimeInGanZhi() == time_gan_zhi:
                        solar_list.append(solar)
                        break
                    solar = solar.next(1)
                    counter += 1
            start_year -= 60
        return solar_list

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
        week = self.__calendar.isoweekday()
        if week == 7:
            week = 0
        return week

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
        festivals = []
        key = "%d-%d" % (self.__month, self.__day)
        if key in SolarUtil.FESTIVAL:
            festivals.append(SolarUtil.FESTIVAL[key])
        week = self.getWeek()
        key = "%d-%d-%d" % (self.__month, int(ceil(self.__day / 7.0)), week)
        if key in SolarUtil.WEEK_FESTIVAL:
            festivals.append(SolarUtil.WEEK_FESTIVAL[key])
        if self.__day + 7 > SolarUtil.getDaysOfMonth(self.__year, self.__month):
            key = "%d-0-%d" % (self.__month, week)
            if key in SolarUtil.WEEK_FESTIVAL:
                festivals.append(SolarUtil.WEEK_FESTIVAL[key])
        return festivals

    def getOtherFestivals(self):
        """
        获取非正式的节日，有可能一天会有多个节日
        :return: 非正式的节日列表，如中元节
        """
        festivals = []
        key = "%d-%d" % (self.__month, self.__day)
        if key in SolarUtil.OTHER_FESTIVAL:
            for f in SolarUtil.OTHER_FESTIVAL[key]:
                festivals.append(f)
        return festivals

    def getXingZuo(self):
        """
        获取星座
        :return: 星座
        """
        index = 11
        y = self.__month * 100 + self.__day
        if 321 <= y <= 419:
            index = 0
        elif 420 <= y <= 520:
            index = 1
        elif 521 <= y <= 621:
            index = 2
        elif 622 <= y <= 722:
            index = 3
        elif 723 <= y <= 822:
            index = 4
        elif 823 <= y <= 922:
            index = 5
        elif 923 <= y <= 1023:
            index = 6
        elif 1024 <= y <= 1122:
            index = 7
        elif 1123 <= y <= 1221:
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
        d = self.__day + ((self.__second / 60.0 + self.__minute) / 60 + self.__hour) / 24
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

    def next(self, days, only_work_day=False):
        """
        获取往后推几天的阳历日期，如果要往前推，则天数用负数
        :param days: 天数
        :param only_work_day: 是否仅工作日
        :return: 阳历日期
        """
        if only_work_day:
            return self.nextWorkday(days)
        c = ExactDate.fromYmdHms(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)
        if days != 0:
            c = c + timedelta(days=days)
        return Solar.fromDate(c)

    def nextWorkday(self, days):
        """
        获取往后推几个工作日的阳历日期，如果要往前推，则天数用负数
        :param days: 天数
        :return: 阳历日期
        """
        c = ExactDate.fromYmdHms(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)
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
                    week = c.isoweekday()
                    if week == 7 or week == 6:
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
        d = self.__day
        if self.__year == 1582 and self.__month == 10:
            if d >= 5:
                d += 10
        return "%04d-%02d-%02d" % (self.__year, self.__month, d)

    def toYmdHms(self):
        return "%s %02d:%02d:%02d" % (self.toYmd(), self.__hour, self.__minute, self.__second)

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
