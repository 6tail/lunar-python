# -*- coding: utf-8 -*-
from datetime import datetime

from .. import Solar
from . import DaYun
from ..util import LunarUtil, SolarUtil


class Yun:
    """
    运
    """

    def __init__(self, eight_char, gender):
        self.__lunar = eight_char.getLunar()
        self.__gender = gender
        yang = 0 == self.__lunar.getYearGanIndexExact() % 2
        man = 1 == gender
        self.__forward = (yang and man) or (not yang and not man)
        self.__compute_start()

    def __compute_start(self):
        """
        起运计算
        """
        prev_jie = self.__lunar.getPrevJie()
        next_jie = self.__lunar.getNextJie()
        current = self.__lunar.getSolar()
        start = current if self.__forward else prev_jie.getSolar()
        end = next_jie.getSolar() if self.__forward else current
        hour_diff = LunarUtil.getTimeZhiIndex(end.toYmdHms()[11: 16]) - LunarUtil.getTimeZhiIndex(start.toYmdHms()[11: 16])
        end_calendar = datetime(end.getYear(), end.getMonth(), end.getDay(), 0, 0, 0, 0)
        start_calendar = datetime(start.getYear(), start.getMonth(), start.getDay(), 0, 0, 0, 0)
        day_diff = (end_calendar - start_calendar).days
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

        year += self.__startYear
        month += self.__startMonth
        if month > 12:
            year += 1
            month -= 12
        day += self.__startDay
        days = SolarUtil.DAYS_OF_MONTH[month - 1]
        if day > days:
            day -= days
            month += 1
        if month > 12:
            year += 1
            month -= 12
        return Solar(year, month, day, 0, 0, 0)

    def getDaYun(self):
        """
        获取大运
        :return: 大运
        """
        n = 10
        da_yun = []
        for i in range(0, n):
            da_yun.append(DaYun(self, i))
        return da_yun
