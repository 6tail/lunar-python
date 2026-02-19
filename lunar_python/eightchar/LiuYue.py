# -*- coding: utf-8 -*-

from ..util import LunarUtil


class LiuYue:
    """
    流月
    """

    def __init__(self, liu_nian, index):
        self.__liuNian = liu_nian
        self.__index = index
        # 预计算干支
        year_gan = liu_nian.getGanZhi()[:1]
        if "甲" == year_gan or "己" == year_gan:
            offset = 2
        elif "乙" == year_gan or "庚" == year_gan:
            offset = 4
        elif "丙" == year_gan or "辛" == year_gan:
            offset = 6
        elif "丁" == year_gan or "壬" == year_gan:
            offset = 8
        else:
            offset = 0
        gan = LunarUtil.GAN[(index + offset) % 10 + 1]
        zhi = LunarUtil.ZHI[(index + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12 + 1]
        self.__ganZhi = gan + zhi

    def getIndex(self):
        return self.__index

    def getMonthInChinese(self):
        """
        获取中文的月
        :return: 中文月，如正
        """
        return LunarUtil.MONTH[self.__index + 1]

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
