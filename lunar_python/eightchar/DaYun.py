# -*- coding: utf-8 -*-
from . import XiaoYun, LiuNian
from ..util import LunarUtil


class DaYun:
    """
    大运
    """

    def __init__(self, yun, index: int):
        self.__yun = yun
        self.__lunar = yun.getLunar()
        self.__index = index
        birth_year = yun.getLunar().getSolar().getYear()
        year = yun.getStartSolar().getYear()
        if index < 1:
            self.__startYear = birth_year
            self.__startAge = 1
            self.__endYear = year - 1
            self.__endAge = year - birth_year
        else:
            add = (index - 1) * 10
            self.__startYear = year + add
            self.__startAge = self.__startYear - birth_year + 1
            self.__endYear = self.__startYear + 9
            self.__endAge = self.__startAge + 9
        # 预计算干支
        if self.__index < 1:
            self.__ganZhi = ""
        else:
            offset = LunarUtil.getJiaZiIndex(self.__lunar.getMonthInGanZhiExact())
            offset += self.__index if self.__yun.isForward() else -self.__index
            size = len(LunarUtil.JIA_ZI)
            if offset >= size:
                offset -= size
            if offset < 0:
                offset += size
            self.__ganZhi = LunarUtil.JIA_ZI[offset]
        # 预计算流年基准偏移量（只查一次节气表）
        self.__liuNianBaseOffset = LunarUtil.getJiaZiIndex(
            self.__lunar.getJieQiTable()["立春"].getLunar().getYearInGanZhiExact()
        )
        # 缓存
        self.__liuNian = None
        self.__xiaoYun = None

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

    def getLiuNianBaseOffset(self):
        """获取流年基准偏移量（供 LiuNian 使用）"""
        return self.__liuNianBaseOffset

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

    def getLiuNian(self, n=10):
        """
        获取流年
        :param n: 轮数
        :return: 流年
        """
        if self.__index < 1:
            n = self.__endYear - self.__startYear + 1
        if self.__liuNian is None or len(self.__liuNian) != n:
            self.__liuNian = [LiuNian(self, i) for i in range(n)]
        return self.__liuNian

    def getXiaoYun(self, n=10):
        """
        获取小运
        :param n: 轮数
        :return: 小运
        """
        if self.__index < 1:
            n = self.__endYear - self.__startYear + 1
        if self.__xiaoYun is None or len(self.__xiaoYun) != n:
            self.__xiaoYun = [XiaoYun(self, i, self.__yun.isForward()) for i in range(n)]
        return self.__xiaoYun
