# -*- coding: utf-8 -*-
from ..util import LunarUtil


class XiaoYun:
    """
    小运
    """

    def __init__(self, daYun, index, forward):
        self.__daYun = daYun
        self.__lunar = daYun.getLunar()
        self.__index = index
        self.__year = daYun.getStartYear() + index
        self.__age = daYun.getStartAge() + index
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
