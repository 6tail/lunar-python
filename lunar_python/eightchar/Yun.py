# -*- coding: utf-8 -*-
from .. import ExactDate, Solar
from . import DaYun
from ..util import LunarUtil, SolarUtil


class Yun:
    """
    运
    """

    def __init__(self, eight_char, gender, sect=1):
        self.__lunar = eight_char.getLunar()
        self.__gender = gender
        yang = 0 == self.__lunar.getYearGanIndexExact() % 2
        man = 1 == gender
        self.__forward = (yang and man) or (not yang and not man)
        self.__compute_start(sect)

    def __compute_start(self, sect):
        """
        起运计算
        """
        prev_jie = self.__lunar.getPrevJie()
        next_jie = self.__lunar.getNextJie()
        current = self.__lunar.getSolar()
        start = current if self.__forward else prev_jie.getSolar()
        end = next_jie.getSolar() if self.__forward else current

        hour = 0

        if 2 == sect:
            minutes = int((end.getCalendar() - start.getCalendar()).total_seconds() / 60)
            year = int(minutes / 4320)
            minutes -= year * 4320
            month = int(minutes / 360)
            minutes -= month * 360
            day = int(minutes / 12)
            minutes -= day * 12
            hour = minutes * 2
        else:
            end_time_zhi_index = 11 if end.getHour() == 23 else LunarUtil.getTimeZhiIndex(end.toYmdHms()[11: 16])
            start_time_zhi_index = 11 if start.getHour() == 23 else LunarUtil.getTimeZhiIndex(start.toYmdHms()[11: 16])
            # 时辰差
            hour_diff = end_time_zhi_index - start_time_zhi_index
            day_diff = ExactDate.getDaysBetween(start.getYear(), start.getMonth(), start.getDay(), end.getYear(), end.getMonth(), end.getDay())
            if hour_diff < 0:
                hour_diff += 12
                day_diff -= 1
            month_diff = int(hour_diff * 10 / 30)
            month = day_diff * 4 + month_diff
            day = hour_diff * 10 - month_diff * 30
            year = int(month / 12)
            month = month - year * 12
        self.__startYear = year
        self.__startMonth = month
        self.__startDay = day
        self.__startHour = hour

    def getGender(self):
        """
        获取性别
        :return: 性别(1男 ， 0女)
        """
        return self.__gender

    def getStartYear(self):
        """
        获取起运年数
        :return: 起运年数
        """
        return self.__startYear

    def getStartMonth(self):
        """
        获取起运月数
        :return: 起运月数
        """
        return self.__startMonth

    def getStartDay(self):
        """
        获取起运天数
        :return: 起运天数
        """
        return self.__startDay

    def getStartHour(self):
        """
        获取起运小时数
        :return: 起运小时数
        """
        return self.__startHour

    def isForward(self):
        """
        是否顺推
        :return: true/false
        """
        return self.__forward

    def getLunar(self):
        return self.__lunar

    def getStartSolar(self):
        """
        获取起运的阳历日期
        :return: 阳历日期
        """
        birth = self.__lunar.getSolar()
        year = birth.getYear()
        month = birth.getMonth()
        day = birth.getDay()
        hour = birth.getHour()

        year += self.__startYear
        month += self.__startMonth
        if month > 12:
            year += 1
            month -= 12
        day += self.__startDay
        hour += self.__startHour
        if hour >= 24:
            hour -= 24
            day += 1
        days = SolarUtil.DAYS_OF_MONTH[month - 1]
        if day > days:
            day -= days
            month += 1
        if month > 12:
            year += 1
            month -= 12
        return Solar(year, month, day, hour, birth.getMinute(), birth.getSecond())

    def getDaYun(self, n=10):
        """
        获取大运
        :param n: 轮数
        :return: 大运
        """
        da_yun = []
        for i in range(0, n):
            da_yun.append(DaYun(self, i))
        return da_yun
