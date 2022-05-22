# -*- coding: utf-8 -*-
from . import NineStar
from .util import LunarUtil


class LunarTime:
    """
    时辰
    """

    def __init__(self, lunar_year, lunar_month, lunar_day, hour, minute, second):
        from . import Lunar
        self.__lunar = Lunar.fromYmdHms(lunar_year, lunar_month, lunar_day, hour, minute, second)
        self.__zhiIndex = LunarUtil.getTimeZhiIndex("%02d:%02d" % (hour, minute))
        self.__ganIndex = (self.__lunar.getDayGanIndexExact() % 5 * 2 + self.__zhiIndex) % 10

    @staticmethod
    def fromYmdHms(lunar_year, lunar_month, lunar_day, hour, minute, second):
        return LunarTime(lunar_year, lunar_month, lunar_day, hour, minute, second)

    def getGan(self):
        return LunarUtil.GAN[self.__ganIndex + 1]

    def getZhi(self):
        return LunarUtil.ZHI[self.__zhiIndex + 1]

    def getGanZhi(self):
        return self.getGan() + self.getZhi()

    def getShengXiao(self):
        return LunarUtil.SHENGXIAO[self.__zhiIndex + 1]

    def getPositionXi(self):
        return LunarUtil.POSITION_XI[self.__ganIndex + 1]

    def getPositionXiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionXi()]

    def getPositionYangGui(self):
        return LunarUtil.POSITION_YANG_GUI[self.__ganIndex + 1]

    def getPositionYangGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYangGui()]

    def getPositionYinGui(self):
        return LunarUtil.POSITION_YIN_GUI[self.__ganIndex + 1]

    def getPositionYinGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYinGui()]

    def getPositionFu(self, sect=2):
        return (LunarUtil.POSITION_FU if 1 == sect else LunarUtil.POSITION_FU_2)[self.__ganIndex + 1]

    def getPositionFuDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getPositionFu(sect)]

    def getPositionCai(self):
        return LunarUtil.POSITION_CAI[self.__ganIndex + 1]

    def getPositionCaiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionCai()]

    def getChong(self):
        return LunarUtil.CHONG[self.__zhiIndex]

    def getChongGan(self):
        return LunarUtil.CHONG_GAN[self.__ganIndex]

    def getChongGanTie(self):
        return LunarUtil.CHONG_GAN_TIE[self.__ganIndex]

    def getChongShengXiao(self):
        chong = self.getChong()
        for i in range(0, len(LunarUtil.ZHI)):
            if LunarUtil.ZHI[i] == chong:
                return LunarUtil.SHENGXIAO[i]
        return ""

    def getChongDesc(self):
        return "(" + self.getChongGan() + self.getChong() + ")" + self.getChongShengXiao()

    def getSha(self):
        return LunarUtil.SHA[self.getZhi()]

    def getNaYin(self):
        return LunarUtil.NAYIN[self.getGanZhi()]

    def getTianShen(self):
        offset = LunarUtil.ZHI_TIAN_SHEN_OFFSET[self.__lunar.getDayZhiExact()]
        return LunarUtil.TIAN_SHEN[(self.__zhiIndex + offset) % 12 + 1]

    def getTianShenType(self):
        return LunarUtil.TIAN_SHEN_TYPE[self.getTianShen()]

    def getTianShenLuck(self):
        return LunarUtil.TIAN_SHEN_TYPE_LUCK[self.getTianShenType()]

    def getYi(self):
        """
        获取时宜
        :return: 宜
        """
        return LunarUtil.getTimeYi(self.__lunar.getDayInGanZhiExact(), self.getGanZhi())

    def getJi(self):
        """
        获取时忌
        :return: 忌
        """
        return LunarUtil.getTimeJi(self.__lunar.getDayInGanZhiExact(), self.getGanZhi())

    def getNineStar(self):
        solar_ymd = self.__lunar.getSolar().toYmd()
        jie_qi = self.__lunar.getJieQiTable()
        asc = False
        if jie_qi["冬至"] <= solar_ymd < jie_qi["夏至"]:
            asc = True
        start = 7 if asc else 3
        day_zhi = self.__lunar.getDayZhi()
        if day_zhi in "子午卯酉":
            start = 1 if asc else 9
        elif day_zhi in "辰戌丑未":
            start = 4 if asc else 6
        index = start + self.__zhiIndex - 1 if asc else start - self.__zhiIndex - 1

        if index > 8:
            index -= 9
        if index < 0:
            index += 9
        return NineStar.fromIndex(index)

    def getGanIndex(self):
        return self.__ganIndex

    def getZhiIndex(self):
        return self.__zhiIndex

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.getGanZhi()

    def getXun(self):
        """
        获取时辰所在旬
        :return: 旬
        """
        return LunarUtil.getXun(self.getGanZhi())

    def getXunKong(self):
        """
        获取值时空亡
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getGanZhi())

    def getMinHm(self):
        hour = self.__lunar.getHour()
        if hour < 1:
            return "00:00"
        elif hour > 22:
            return "23:00"
        return "%02d:00" % (hour - 1 if hour % 2 == 0 else hour)

    def getMaxHm(self):
        hour = self.__lunar.getHour()
        if hour < 1:
            return "00:59"
        elif hour > 22:
            return "23:59"
        return "%02d:59" % (hour + 1 if hour % 2 != 0 else hour)
