# -*- coding: utf-8 -*-
from . import XiaoYun
from . import LiuNian
from ..util import LunarUtil


class DaYun:
    """
    大运
    """

    def __init__(self, yun, index):
        self.__yun = yun
        self.__lunar = yun.getLunar()
        self.__index = index
        year = yun.getStartSolar().getYear()
        if index < 1:
            self.__startYear = self.__lunar.getSolar().getYear()
            self.__startAge = 1
            self.__endYear = year - 1
            self.__endAge = yun.getStartYear()
        else:
            add = (index - 1) * 10
            self.__startYear = year + add
            self.__startAge = yun.getStartYear() + add + 1
            self.__endYear = self.__startYear + 9
            self.__endAge = self.__startAge + 9

    def getStartYear(self):
        return self.__startYear

    def getEndYear(self):
        return self.__endYear

    def getStartAge(self):
        return self.__startAge

    def getEndAge(self):
        return self.__endAge

    def getIndex(self):
        return self.__index

    def getLunar(self):
        return self.__lunar

    def getGanZhi(self):

        """
        获取干支
        :return: 干支
        """
        if self.__index < 1:
            return ""
        offset = LunarUtil.getJiaZiIndex(self.__lunar.getMonthInGanZhiExact())
        offset += self.__index if self.__yun.isForward() else self.__index
        size = len(LunarUtil.JIA_ZI)
        if offset >= size:
            offset -= size
        if offset < 0:
            offset += size
        return LunarUtil.JIA_ZI[offset]

    def getLiuNian(self):

        """
        获取流年
        :return: 流年
        """
        n = 10
        if self.__index < 1:
            n = self.__endYear - self.__startYear + 1
        liu_nian = []
        for i in range(0, n):
            liu_nian.append(LiuNian(self, i))
        return liu_nian

    def getXiaoYun(self):

        """
        获取小运
        :return: 小运
        """
        n = 10
        if self.__index < 1:
            n = self.__endYear - self.__startYear + 1
        xiao_yun = []
        for i in range(0, n):
            xiao_yun.append(XiaoYun(self, i, self.__yun.isForward()))
        return xiao_yun
