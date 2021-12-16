# -*- coding: utf-8 -*-
from . import Lunar, LunarMonth
from .util import LunarUtil, FotoUtil


class Foto:
    """
    佛历
    """

    DEAD_YEAR = -543

    def __init__(self, lunar):
        self.__lunar = lunar

    @staticmethod
    def fromLunar(lunar):
        return Foto(lunar)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return Foto.fromLunar(Lunar.fromYmdHms(year + Foto.DEAD_YEAR - 1, month, day, hour, minute, second))

    @staticmethod
    def fromYmd(year, month, day):
        return Foto.fromYmdHms(year, month, day, 0, 0, 0)

    def getLunar(self):
        return self.__lunar

    def getYear(self):
        sy = self.__lunar.getSolar().getYear()
        y = sy - Foto.DEAD_YEAR
        if sy == self.__lunar.getYear():
            y += 1
        return y

    def getMonth(self):
        return self.__lunar.getMonth()

    def getDay(self):
        return self.__lunar.getDay()

    def getYearInChinese(self):
        y = str(self.getYear())
        s = ""
        for i in range(0, len(y)):
            s += LunarUtil.NUMBER[ord(y[i]) - 48]
        return s

    def getMonthInChinese(self):
        return self.__lunar.getMonthInChinese()

    def getDayInChinese(self):
        return self.__lunar.getDayInChinese()

    def getFestivals(self):
        festivals = []
        md = "%d-%d" % (self.getMonth(), self.getDay())
        if md in FotoUtil.FESTIVAL:
            fs = FotoUtil.FESTIVAL[md]
            for f in fs:
                festivals.append(f)
        return festivals

    def isMonthZhai(self):
        m = self.getMonth()
        return 1 == m or 5 == m or 9 == m

    def isDayYangGong(self):
        for f in self.getFestivals():
            if "杨公忌" == f.getName():
                return True
        return False

    def isDayZhaiShuoWang(self):
        d = self.getDay()
        return 1 == d or 15 == d

    def isDayZhaiSix(self):
        d = self.getDay()
        if 8 == d or 14 == d or 15 == d or 23 == d or 29 == d or 30 == d:
            return True
        elif 28 == d:
            m = LunarMonth.fromYm(self.__lunar.getYear(), self.getMonth())
            return m is not None and 30 != m.getDayCount()
        return False

    def isDayZhaiTen(self):
        d = self.getDay()
        return 1 == d or 8 == d or 14 == d or 15 == d or 18 == d or 23 == d or 24 == d or 28 == d or 29 == d or 30 == d

    def isDayZhaiGuanYin(self):
        k = "%d-%d" % (self.getMonth(), self.getDay())
        for d in FotoUtil.DAY_ZHAI_GUAN_YIN:
            if k == d:
                return True
        return False

    def getXiu(self):
        return FotoUtil.getXiu(self.getMonth(), self.getDay())

    def getXiuLuck(self):
        return LunarUtil.XIU_LUCK[self.getXiu()]

    def getXiuSong(self):
        return LunarUtil.XIU_SONG[self.getXiu()]

    def getZheng(self):
        return LunarUtil.ZHENG[self.getXiu()]

    def getAnimal(self):
        return LunarUtil.ANIMAL[self.getXiu()]

    def getGong(self):
        return LunarUtil.GONG[self.getXiu()]

    def getShou(self):
        return LunarUtil.SHOU[self.getGong()]

    def __str__(self):
        return self.toString()

    def toString(self):
        return "%s年%s月%s" % (self.getYearInChinese(), self.getMonthInChinese(), self.getDayInChinese())

    def toFullString(self):
        s = self.toString()
        for f in self.getFestivals():
            s += " (%s)" % f
        return s
