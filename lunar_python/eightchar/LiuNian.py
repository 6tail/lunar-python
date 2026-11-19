# -*- coding: utf-8 -*-
from . import LiuYue
from ..util import LunarUtil


class LiuNian:
    """
    流年
    """

    def __init__(self, da_yun, index):
        self.__daYun = da_yun
        self.__index = index
        self.__year = da_yun.getStartYear() + index
        self.__age = da_yun.getStartAge() + index
        # 使用 DaYun 预计算的基准偏移量，避免重复查节气表
        offset = da_yun.getLiuNianBaseOffset() + self.__index
        if da_yun.getIndex() > 0:
            offset += da_yun.getStartAge() - 1
        offset %= len(LunarUtil.JIA_ZI)
        self.__ganZhi = LunarUtil.JIA_ZI[offset]
        self.__liuYue = None

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
        return self.__ganZhi

    def getXun(self):
        """
        获取所在旬
        :return: 旬
        """
        return LunarUtil.getXun(self.__ganZhi)

    def getXunKong(self):
        """
        获取旬空(空亡)
        :return: 旬空(空亡)
        """
        return LunarUtil.getXunKong(self.__ganZhi)

    def getLiuYue(self):
        """
        获取流月
        :return: 流月
        """
        if self.__liuYue is None:
            self.__liuYue = [LiuYue(self, i) for i in range(12)]
        return self.__liuYue
