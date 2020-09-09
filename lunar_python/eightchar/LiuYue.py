# -*- coding: utf-8 -*-
from ..util import LunarUtil


class LiuYue:
    """
    流月
    """

    def __init__(self, liuNian, index):
        self.__liuNian = liuNian
        self.__index = index

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
        <p>
        《五虎遁》
        甲己之年丙作首，
        乙庚之年戊为头，
        丙辛之年寻庚上，
        丁壬壬寅顺水流，
        若问戊癸何处走，
        甲寅之上好追求。
        :return: 干支
        """
        offset = 0
        yearGanZhi = self.__liuNian.getGanZhi()
        yearGan = yearGanZhi[0: len(yearGanZhi) / 2]
        if "甲" == yearGan or "己" == yearGan:
            offset = 2
        elif "乙" == yearGan or "庚" == yearGan:
            offset = 4
        elif "丙" == yearGan or "辛" == yearGan:
            offset = 6
        elif "丁" == yearGan or "壬" == yearGan:
            offset = 8
        gan = LunarUtil.GAN[(self.__index + offset) % 10 + 1]
        zhi = LunarUtil.ZHI[(self.__index + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12 + 1]
        return gan + zhi
