# -*- coding: utf-8 -*-
from ..util import LunarUtil


class XiaoYun:
    """
    小运
    """

    def __init__(self, da_yun, index, forward):
        self.__daYun = da_yun
        self.__lunar = da_yun.getLunar()
        self.__index = index
        self.__year = da_yun.getStartYear() + index
        self.__age = da_yun.getStartAge() + index
        self.__forward = forward

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
        offset = LunarUtil.getJiaZiIndex(self.__lunar.getTimeInGanZhi())
        add = self.__index + 1
        if self.__daYun.getIndex() > 0:
            add += self.__daYun.getStartAge() - 1
        offset += add if self.__forward else add
        size = len(LunarUtil.JIA_ZI)
        while offset < 0:
            offset += size
        offset %= size
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
