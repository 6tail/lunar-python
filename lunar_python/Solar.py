# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta
from math import ceil

from .exceptions import SolarDateException
from .util import SolarUtil, LunarUtil, HolidayUtil, TimeZoneUtil


class Solar:
    """
    阳历日期
    
    支持时区/夏令时处理。默认时区为 Asia/Shanghai（包含1986-1991中国夏令时历史）。
    
    时区支持说明：
    - 所有时间输入默认按 Asia/Shanghai 时区解释（包含历史DST规则）
    - 可通过 tz 参数指定其他时区（IANA字符串或tzinfo对象）
    - 内部存储为指定时区的本地时间，同时保存时区信息用于UTC转换
    
    中国夏令时历史（1986-1991）：
    - 这些年份的夏令时期间，北京时间为 UTC+9
    - 1991年9月15日后，中国不再实行夏令时，统一使用 UTC+8
    """

    # 2000年儒略日数(2000-1-1 12:00:00 UTC)
    J2000 = 2451545

    def __init__(self, year, month, day, hour, minute, second, tz=None):
        """
        构造阳历日期
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param hour: 时
        :param minute: 分
        :param second: 秒
        :param tz: 时区，可以是 IANA 字符串（如 "Asia/Shanghai"）或 tzinfo 对象，
                   默认为 None 表示使用 Asia/Shanghai
        """
        if year == 1582 and month == 10:
            if 4 < day < 15:
                raise SolarDateException("wrong solar year %d month %d day %d" % (year, month, day))
        if month < 1 or month > 12:
            raise SolarDateException("wrong month %d" % month)
        if day < 1 or month > 31:
            raise SolarDateException("wrong day %d" % day)
        if hour < 0 or hour > 23:
            raise SolarDateException("wrong hour %d" % hour)
        if minute < 0 or minute > 59:
            raise SolarDateException("wrong minute %d" % minute)
        if second < 0 or second > 59:
            raise SolarDateException("wrong second %d" % second)
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__tz = tz  # 存储时区（None 表示默认 Asia/Shanghai）

    @staticmethod
    def fromDate(date, tz=None):
        """
        从 datetime 对象创建阳历日期
        
        :param date: datetime 对象（naive 或 aware）
        :param tz: 目标时区。如果 date 是 aware 的，会先转换到此时区；
                   如果 date 是 naive 的，按此时区解释。
                   默认为 Asia/Shanghai。
        :return: Solar 对象
        """
        if date.tzinfo is not None:
            # aware datetime: 转换到目标时区后提取时间分量
            target_tz = TimeZoneUtil.get_timezone(tz)
            local_dt = date.astimezone(target_tz)
            return Solar(local_dt.year, local_dt.month, local_dt.day,
                        local_dt.hour, local_dt.minute, local_dt.second, tz)
        else:
            # naive datetime: 直接按指定时区解释
            return Solar(date.year, date.month, date.day,
                        date.hour, date.minute, date.second, tz)

    @staticmethod
    def fromJulianDay(julian_day, tz=None):
        """
        从儒略日创建阳历日期
        
        注意：儒略日基于 UTC，此方法会根据指定时区转换为本地时间。
        
        :param julian_day: 儒略日（UTC）
        :param tz: 目标时区，默认为 Asia/Shanghai
        :return: Solar 对象
        """
        # 儒略日转 UTC 时间
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
        if hour > 23:
            hour -= 24
            day += 1
        
        # UTC 时间转目标时区
        utc_dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
        target_tz = TimeZoneUtil.get_timezone(tz)
        local_dt = utc_dt.astimezone(target_tz)
        
        return Solar(local_dt.year, local_dt.month, local_dt.day,
                    local_dt.hour, local_dt.minute, local_dt.second, tz)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second, tz=None):
        """
        从年月日时分秒创建阳历日期
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param hour: 时
        :param minute: 分
        :param second: 秒
        :param tz: 时区，默认为 Asia/Shanghai
        :return: Solar 对象
        """
        return Solar(year, month, day, hour, minute, second, tz)

    @staticmethod
    def fromYmd(year, month, day, tz=None):
        """
        从年月日创建阳历日期（时间为 00:00:00）
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param tz: 时区，默认为 Asia/Shanghai
        :return: Solar 对象
        """
        return Solar(year, month, day, 0, 0, 0, tz)

    @staticmethod
    def fromBaZi(year_gan_zhi, month_gan_zhi, day_gan_zhi, time_gan_zhi, sect=2, base_year=1900):
        from . import Lunar
        sect = 1 if 1 == sect else 2
        solar_list = []
        # 月地支距寅月的偏移值
        m = LunarUtil.find(month_gan_zhi[1:], LunarUtil.ZHI, -1) - 2
        if m < 0:
            m += 12
        # 月天干要一致
        if ((LunarUtil.find(year_gan_zhi[:1], LunarUtil.GAN, -1) + 1) * 2 + m) % 10 != LunarUtil.find(month_gan_zhi[:1], LunarUtil.GAN, -1):
            return solar_list
        # 1年的立春是辛酉，序号57
        y = LunarUtil.getJiaZiIndex(year_gan_zhi) - 57
        if y < 0:
            y += 60
        y += 1
        # 节令偏移值
        m *= 2
        # 时辰地支转时刻，子时按零点算
        h = LunarUtil.find(time_gan_zhi[1:], LunarUtil.ZHI, -1) * 2
        hours = [h]
        if 0 == h and 2 == sect:
            hours.append(23)
        start_year = base_year - 1

        # 结束年
        end_year = datetime.now().year

        while y <= end_year:
            if y >= start_year:
                # 立春为寅月的开始
                jie_qi_table = Lunar.fromYmd(y, 1, 1).getJieQiTable()
                # 节令推移，年干支和月干支就都匹配上了
                solar_time = jie_qi_table[Lunar.JIE_QI_IN_USE[4 + m]]
                if solar_time.getYear() >= base_year:
                    # 日干支和节令干支的偏移值
                    d = LunarUtil.getJiaZiIndex(day_gan_zhi) - LunarUtil.getJiaZiIndex(solar_time.getLunar().getDayInGanZhiExact2())
                    if d < 0:
                        d += 60
                    if d > 0:
                        # 从节令推移天数
                        solar_time = solar_time.next(d)
                    for hour in hours:
                        mi = 0
                        s = 0
                        if d == 0 and hour == solar_time.getHour():
                            # 如果正好是节令当天，且小时和节令的小时数相等的极端情况，把分钟和秒钟带上
                            mi = solar_time.getMinute()
                            s = solar_time.getSecond()
                        # 验证一下
                        solar = Solar.fromYmdHms(solar_time.getYear(), solar_time.getMonth(), solar_time.getDay(), hour, mi, s)
                        if d == 30:
                            solar = solar.nextHour(-1)
                        lunar = solar.getLunar()
                        dgz = lunar.getDayInGanZhiExact2() if 2 == sect else lunar.getDayInGanZhiExact()
                        if lunar.getYearInGanZhiExact() == year_gan_zhi and lunar.getMonthInGanZhiExact() == month_gan_zhi and dgz == day_gan_zhi and lunar.getTimeInGanZhi() == time_gan_zhi:
                            solar_list.append(solar)
            y += 60
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
        return (int(self.getJulianDay() + 0.5) + 7000001) % 7

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
        获取儒略日（UTC）
        
        此方法会将本地时间转换为 UTC 后计算儒略日。
        
        :return: 儒略日
        """
        # 获取 UTC 时间
        utc_dt = self.toUTC()
        y = utc_dt.year
        m = utc_dt.month
        d = utc_dt.day + ((utc_dt.second / 60.0 + utc_dt.minute) / 60 + utc_dt.hour) / 24
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
    
    def getJulianDayLocal(self):
        """
        获取基于本地时间的儒略日（不转换时区，兼容旧版本行为）
        
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
        return Lunar.fromSolar(self)

    def nextDay(self, days):
        y = self.__year
        m = self.__month
        d = self.__day
        if 1582 == y and 10 == m:
            if d > 4:
                d -= 10
        if days > 0:
            d += days
            days_in_month = SolarUtil.getDaysOfMonth(y, m)
            while d > days_in_month:
                d -= days_in_month
                m += 1
                if m > 12:
                    m = 1
                    y += 1
                days_in_month = SolarUtil.getDaysOfMonth(y, m)
        elif days < 0:
            while d + days <= 0:
                m -= 1
                if m < 1:
                    m = 12
                    y -= 1
                d += SolarUtil.getDaysOfMonth(y, m)
            d += days
        if 1582 == y and 10 == m:
            if d > 4:
                d += 10
        return Solar.fromYmdHms(y, m, d, self.__hour, self.__minute, self.__second, self.__tz)

    def next(self, days, only_work_day=False):
        """
        获取往后推几天的阳历日期，如果要往前推，则天数用负数
        :param days: 天数
        :param only_work_day: 是否仅工作日
        :return: 阳历日期
        """
        if not only_work_day:
            return self.nextDay(days)
        solar = Solar.fromYmdHms(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second, self.__tz)
        if days != 0:
            rest = abs(days)
            add = 1
            if days < 0:
                add = -1
            while rest > 0:
                solar = solar.next(add)
                work = True
                holiday = HolidayUtil.getHoliday(solar.getYear(), solar.getMonth(), solar.getDay())
                if holiday is None:
                    week = solar.getWeek()
                    if 0 == week or 6 == week:
                        work = False
                else:
                    work = holiday.isWork()
                if work:
                    rest -= 1
        return solar

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
    
    def getTimezone(self):
        """
        获取时区
        
        :return: 时区（None 表示默认 Asia/Shanghai）
        """
        return self.__tz
    
    def getTimezoneInfo(self):
        """
        获取时区信息对象
        
        :return: tzinfo 对象
        """
        return TimeZoneUtil.get_timezone(self.__tz)
    
    def toUTC(self):
        """
        转换为 UTC 时间
        
        :return: UTC 时间的 datetime 对象（aware）
        """
        local_dt = datetime(self.__year, self.__month, self.__day,
                           self.__hour, self.__minute, self.__second)
        return TimeZoneUtil.to_utc(local_dt, self.__tz)
    
    def toDatetime(self):
        """
        转换为带时区的 datetime 对象
        
        :return: datetime 对象（aware）
        """
        dt = datetime(self.__year, self.__month, self.__day,
                     self.__hour, self.__minute, self.__second)
        return TimeZoneUtil.ymdhms_to_datetime(
            self.__year, self.__month, self.__day,
            self.__hour, self.__minute, self.__second, self.__tz)
    
    def toTimezone(self, tz):
        """
        转换到另一个时区
        
        :param tz: 目标时区（IANA 字符串或 tzinfo 对象）
        :return: 新的 Solar 对象
        """
        utc_dt = self.toUTC()
        target_tz = TimeZoneUtil.get_timezone(tz)
        local_dt = utc_dt.astimezone(target_tz)
        return Solar(local_dt.year, local_dt.month, local_dt.day,
                    local_dt.hour, local_dt.minute, local_dt.second, tz)
    
    def getUTCOffset(self):
        """
        获取当前时间点的 UTC 偏移小时数
        
        会考虑夏令时规则。
        
        :return: UTC 偏移小时数（如 +8, +9, -5 等）
        """
        dt = datetime(self.__year, self.__month, self.__day,
                     self.__hour, self.__minute, self.__second)
        return TimeZoneUtil.get_utc_offset_hours(dt, self.__tz)
    
    def isDST(self):
        """
        检查当前时间是否处于夏令时
        
        :return: True 如果处于夏令时，否则 False
        """
        dt = datetime(self.__year, self.__month, self.__day,
                     self.__hour, self.__minute, self.__second)
        return TimeZoneUtil.is_dst(dt, self.__tz)
    
    def toTrueSolarTime(self, longitude):
        """
        转换为真太阳时
        
        真太阳时（True Solar Time）是基于太阳实际位置计算的时间，
        考虑了：
        1. 当地经度与时区标准子午线的差异
        2. 时差方程（地球轨道椭圆和地轴倾斜导致的修正）
        
        这对于精确的八字排盘非常重要，因为传统命理学基于太阳位置。
        
        :param longitude: 当地经度，可以是：
            - float/int: 经度值（东经为正，西经为负）
            - str: 城市名称（如 "北京", "上海", "New York"）
        :return: 新的 Solar 对象（真太阳时）
        
        示例：
            # 北京标准时间转换为北京真太阳时（经度 116.4°）
            solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
            true_solar = solar.toTrueSolarTime(116.4)
            # 或使用城市名
            true_solar = solar.toTrueSolarTime("北京")
        """
        dt = datetime(self.__year, self.__month, self.__day,
                     self.__hour, self.__minute, self.__second)
        true_dt = TimeZoneUtil.to_true_solar_time(dt, longitude, self.__tz)
        return Solar(true_dt.year, true_dt.month, true_dt.day,
                    true_dt.hour, true_dt.minute, true_dt.second, self.__tz)
    
    def getTrueSolarTimeInfo(self, longitude):
        """
        获取真太阳时详细信息
        
        :param longitude: 当地经度（城市名或经度值）
        :return: dict 包含：
            - standard_time: 标准时间
            - true_solar_time: 真太阳时
            - longitude: 经度
            - standard_meridian: 时区标准子午线经度
            - longitude_offset_minutes: 经度偏移（分钟）
            - equation_of_time_minutes: 时差方程（分钟）
            - total_offset_minutes: 总偏移（分钟）
        """
        return TimeZoneUtil.get_true_solar_time_info(
            self.__year, self.__month, self.__day,
            self.__hour, self.__minute, longitude, self.__tz
        )
    
    @staticmethod
    def fromTrueSolarTime(year, month, day, hour, minute, second, longitude, tz=None):
        """
        从真太阳时创建 Solar 对象（转换为标准时间存储）
        
        当用户提供的是真太阳时（如根据日晷读取的时间），
        使用此方法可以正确转换为标准时间。
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param hour: 时
        :param minute: 分
        :param second: 秒
        :param longitude: 当地经度（城市名或经度值）
        :param tz: 时区
        :return: Solar 对象（标准时间）
        """
        dt = datetime(year, month, day, hour, minute, second)
        standard_dt = TimeZoneUtil.from_true_solar_time(dt, longitude, tz)
        return Solar(standard_dt.year, standard_dt.month, standard_dt.day,
                    standard_dt.hour, standard_dt.minute, standard_dt.second, tz)

    def toYmd(self):
        return "%04d-%02d-%02d" % (self.__year, self.__month, self.__day)

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

    def subtract(self, solar):
        return SolarUtil.getDaysBetween(solar.getYear(), solar.getMonth(), solar.getDay(), self.__year, self.__month, self.__day)

    def subtractMinute(self, solar):
        days = self.subtract(solar)
        cm = self.__hour * 60 + self.__minute
        sm = solar.getHour() * 60 + solar.getMinute()
        m = cm - sm
        if m < 0:
            m += 1440
            days -= 1
        m += days * 1440
        return m

    def isAfter(self, solar):
        if self.__year > solar.getYear():
            return True
        if self.__year < solar.getYear():
            return False
        if self.__month > solar.getMonth():
            return True
        if self.__month < solar.getMonth():
            return False
        if self.__day > solar.getDay():
            return True
        if self.__day < solar.getDay():
            return False
        if self.__hour > solar.getHour():
            return True
        if self.__hour < solar.getHour():
            return False
        if self.__minute > solar.getMinute():
            return True
        if self.__minute < solar.getMinute():
            return False
        return self.__second > solar.getSecond()

    def isBefore(self, solar):
        if self.__year > solar.getYear():
            return False
        if self.__year < solar.getYear():
            return True
        if self.__month > solar.getMonth():
            return False
        if self.__month < solar.getMonth():
            return True
        if self.__day > solar.getDay():
            return False
        if self.__day < solar.getDay():
            return True
        if self.__hour > solar.getHour():
            return False
        if self.__hour < solar.getHour():
            return True
        if self.__minute > solar.getMinute():
            return False
        if self.__minute < solar.getMinute():
            return True
        return self.__second < solar.getSecond()

    def nextYear(self, years):
        y = self.__year + years
        m = self.__month
        d = self.__day
        if 1582 == y and 10 == m:
            if 4 < d < 15:
                d += 10
        elif 2 == m:
            if d > 28:
                if not SolarUtil.isLeapYear(y):
                    d = 28
        return Solar.fromYmdHms(y, m, d, self.__hour, self.__minute, self.__second, self.__tz)

    def nextMonth(self, months):
        from . import SolarMonth
        month = SolarMonth.fromYm(self.__year, self.__month).next(months)
        y = month.getYear()
        m = month.getMonth()
        d = self.__day
        if 1582 == y and 10 == m:
            if 4 < d < 15:
                d += 10
        else:
            days = SolarUtil.getDaysOfMonth(y, m)
            if d > days:
                d = days
        return Solar.fromYmdHms(y, m, d, self.__hour, self.__minute, self.__second, self.__tz)

    def nextHour(self, hours):
        h = self.__hour + hours
        n = 1
        if h < 0:
            n = -1
        hour = abs(h)
        days = int(hour / 24) * n
        hour = (hour % 24) * n
        if hour < 0:
            hour += 24
            days -= 1
        solar = self.next(days)
        return Solar.fromYmdHms(solar.getYear(), solar.getMonth(), solar.getDay(), hour, solar.getMinute(), solar.getSecond(), self.__tz)
