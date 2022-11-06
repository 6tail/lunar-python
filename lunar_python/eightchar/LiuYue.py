# -*- coding: utf-8 -*-

from ..util import LunarUtil


class LiuYue:
    """
    流月
    """

    def __init__(self, liu_nian, index):
        self.__liuNian = liu_nian
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
        year_gan_zhi = self.__liuNian.getGanZhi()
        year_gan = year_gan_zhi[:1]
        if "甲" == year_gan or "己" == year_gan:
            offset = 2
        elif "乙" == year_gan or "庚" == year_gan:
            offset = 4
        elif "丙" == year_gan or "辛" == year_gan:
            offset = 6
        elif "丁" == year_gan or "壬" == year_gan:
            offset = 8
        gan = LunarUtil.GAN[(self.__index + offset) % 10 + 1]
        zhi = LunarUtil.ZHI[(self.__index + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12 + 1]
        return gan + zhi

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
