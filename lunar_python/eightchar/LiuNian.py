# -*- coding: utf-8 -*-
from . import LiuYue
from ..util import LunarUtil


class LiuNian:
    """
    流年
    """

    def __init__(self, da_yun, index):
        self.__daYun = da_yun
        self.__lunar = da_yun.getLunar()
        self.__index = index
        self.__year = da_yun.getStartYear() + index
        self.__age = da_yun.getStartAge() + index

    def getIndex(self):
        return self.__index

    def getYear(self):
        return self.__year

    def getAge(self):
        return self.__age

    def getGanZhi(self):
        """
        获取干支
        :return: 干支
        """
        offset = LunarUtil.getJiaZiIndex(self.__lunar.getJieQiTable()["立春"].getLunar().getYearInGanZhiExact()) + self.__index
        if self.__daYun.getIndex() > 0:
            offset += self.__daYun.getStartAge() - 1
        offset %= len(LunarUtil.JIA_ZI)
        return LunarUtil.JIA_ZI[offset]

    def getXun(self):
        """
        获取所在旬
        :return: 旬
        """
        return LunarUtil.getXun(self.getGanZhi())

    def getXunKong(self):
        """
        获取旬空(空亡)
        :return: 旬空(空亡)
        """
        return LunarUtil.getXunKong(self.getGanZhi())

    def getLiuYue(self):
        """
        获取流月
        :return: 流月
        """
        n = 12
        liu_yue = []
        for i in range(0, n):
            liu_yue.append(LiuYue(self, i))
        return liu_yue
