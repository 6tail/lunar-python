# -*- coding: utf-8 -*-
from . import Solar, NineStar
from .util import ShouXingUtil, LunarUtil


class LunarYear:
    """
    农历年
    """

    YUAN = ("下", "上", "中")

    YUN = ("七", "八", "九", "一", "二", "三", "四", "五", "六")

    __LEAP_11 = (75, 94, 170, 238, 265, 322, 389, 469, 553, 583, 610, 678, 735, 754, 773, 849, 887, 936, 1050, 1069, 1126, 1145, 1164, 1183, 1259, 1278, 1308, 1373, 1403, 1441, 1460, 1498, 1555, 1593, 1612, 1631, 1642, 2033, 2128, 2147, 2242, 2614, 2728, 2910, 3062, 3244, 3339, 3616, 3711, 3730, 3825, 4007, 4159, 4197, 4322, 4341, 4379, 4417, 4531, 4599, 4694, 4713, 4789, 4808, 4971, 5085, 5104, 5161, 5180, 5199, 5294, 5305, 5476, 5677, 5696, 5772, 5791, 5848, 5886, 6049, 6068, 6144, 6163, 6258, 6402, 6440, 6497, 6516, 6630, 6641, 6660, 6679, 6736, 6774, 6850, 6869, 6899, 6918, 6994, 7013, 7032, 7051, 7070, 7089, 7108, 7127, 7146, 7222, 7271, 7290, 7309, 7366, 7385, 7404, 7442, 7461, 7480, 7491, 7499, 7594, 7624, 7643, 7662, 7681, 7719, 7738, 7814, 7863, 7882, 7901, 7939, 7958, 7977, 7996,
                 8034, 8053, 8072, 8091, 8121, 8159, 8186, 8216, 8235, 8254, 8273, 8311, 8330, 8341, 8349, 8368, 8444, 8463, 8474, 8493, 8531, 8569, 8588, 8626, 8664, 8683, 8694, 8702, 8713, 8721, 8751, 8789, 8808, 8816, 8827, 8846, 8884, 8903, 8922, 8941, 8971, 9036, 9066, 9085, 9104, 9123, 9142, 9161, 9180, 9199, 9218, 9256, 9294, 9313, 9324, 9343, 9362, 9381, 9419, 9438, 9476, 9514, 9533, 9544, 9552, 9563, 9571, 9582, 9601, 9639, 9658, 9666, 9677, 9696, 9734, 9753, 9772, 9791, 9802, 9821, 9886, 9897, 9916, 9935, 9954, 9973, 9992)

    __LEAP_12 = (37, 56, 113, 132, 151, 189, 208, 227, 246, 284, 303, 341, 360, 379, 417, 436, 458, 477, 496, 515, 534, 572, 591, 629, 648, 667, 697, 716, 792, 811, 830, 868, 906, 925, 944, 963, 982, 1001, 1020, 1039, 1058, 1088, 1153, 1202, 1221, 1240, 1297, 1335, 1392, 1411, 1422, 1430, 1517, 1525, 1536, 1574, 3358, 3472, 3806, 3988, 4751, 4941, 5066, 5123, 5275, 5343, 5438, 5457, 5495, 5533, 5552, 5715, 5810, 5829, 5905, 5924, 6421, 6535, 6793, 6812, 6888, 6907, 7002, 7184, 7260, 7279, 7374, 7556, 7746, 7757, 7776, 7833, 7852, 7871, 7966, 8015, 8110, 8129, 8148, 8224, 8243, 8338, 8406, 8425, 8482, 8501, 8520, 8558, 8596, 8607, 8615, 8645, 8740, 8778, 8835, 8865, 8930, 8960, 8979, 8998, 9017, 9055, 9074, 9093, 9112, 9150, 9188, 9237, 9275, 9332, 9351, 9370, 9408, 9427, 9446, 9457, 9465,
                 9495, 9560, 9590, 9628, 9647, 9685, 9715, 9742, 9780, 9810, 9818, 9829, 9848, 9867, 9905, 9924, 9943, 9962, 10000)

    __LEAP = {}

    __CACHE = {}

    for i in range(0, len(__LEAP_11)):
        __LEAP[__LEAP_11[i]] = 13
    for i in range(0, len(__LEAP_12)):
        __LEAP[__LEAP_12[i]] = 14

    def __init__(self, lunar_year):
        self.__year = lunar_year
        offset = lunar_year - 4
        year_gan_index = offset % 10
        year_zhi_index = offset % 12
        if year_gan_index < 0:
            year_gan_index += 10
        if year_zhi_index < 0:
            year_zhi_index += 12
        self.__ganIndex = year_gan_index
        self.__zhiIndex = year_zhi_index
        self.__months = []
        self.__jieQiJulianDays = []
        self.compute()

    @staticmethod
    def fromYear(lunar_year):
        if lunar_year not in LunarYear.__CACHE:
            obj = LunarYear(lunar_year)
            LunarYear.__CACHE[lunar_year] = obj
        else:
            obj = LunarYear.__CACHE[lunar_year]
        return obj

    def compute(self):
        from . import Lunar, Solar, LunarMonth
        # 节气(中午12点)，长度27
        jq = []
        # 合朔，即每月初一(中午12点)，长度16
        hs = []
        # 每月天数，长度15
        day_counts = []

        current_year = self.__year
        year = current_year - 2000

        # 从上年的大雪到下年的立春
        for i in range(0, len(Lunar.JIE_QI_IN_USE)):
            # 精确的节气
            t = 36525 * ShouXingUtil.saLonT((year + (17 + i) * 15.0 / 360) * ShouXingUtil.PI_2)
            t += ShouXingUtil.ONE_THIRD - ShouXingUtil.dtT(t)
            self.__jieQiJulianDays.append(t + Solar.J2000)
            # 按中午12点算的节气
            if 0 < i < 26:
                jq.append(round(t))
        # 冬至前的初一
        w = ShouXingUtil.calcShuo(jq[0])
        if w > jq[0]:
            w -= 29.5306
        # 递推每月初一
        for i in range(0, 16):
            hs.append(ShouXingUtil.calcShuo(w + 29.5306 * i))
        # 每月天数
        for i in range(0, 15):
            day_counts.append(int(hs[i + 1] - hs[i]))

        current_year_leap = -1
        if current_year in LunarYear.__LEAP:
            current_year_leap = LunarYear.__LEAP[current_year]
        else:
            if hs[13] <= jq[24]:
                i = 1
                while hs[i + 1] > jq[2 * i] and i < 13:
                    i += 1
                current_year_leap = i

        prev_year = current_year - 1
        prev_year_leap = -1
        if prev_year in LunarYear.__LEAP:
            prev_year_leap = LunarYear.__LEAP[prev_year] - 12

        y = prev_year
        m = 11
        for i in range(0, 15):
            cm = m
            is_next_leap = False
            if y == current_year and i == current_year_leap:
                cm = -m
            elif y == prev_year and i == prev_year_leap:
                cm = -m
            if y == current_year and i + 1 == current_year_leap:
                is_next_leap = True
            elif y == prev_year and i + 1 == prev_year_leap:
                is_next_leap = True
            self.__months.append(LunarMonth(y, cm, day_counts[i], hs[i] + Solar.J2000))
            if not is_next_leap:
                m += 1
            if m == 13:
                m = 1
                y += 1

    def getYear(self):
        return self.__year

    def getGanIndex(self):
        return self.__ganIndex

    def getZhiIndex(self):
        return self.__zhiIndex

    def getGan(self):
        return LunarUtil.GAN[self.__ganIndex + 1]

    def getZhi(self):
        return LunarUtil.ZHI[self.__zhiIndex + 1]

    def getGanZhi(self):
        return self.getGan() + self.getZhi()

    def toString(self):
        return str(self.__year) + ""

    def toFullString(self):
        return "%d年" % self.__year

    def __str__(self):
        return self.toString()

    def getMonths(self):
        return self.__months

    def getJieQiJulianDays(self):
        return self.__jieQiJulianDays

    def getLeapMonth(self):
        """
        获取闰月
        :return: 闰月数字，1代表闰1月，0代表无闰月
        """
        for i in range(0, len(self.__months)):
            m = self.__months[i]
            if m.getYear() == self.__year and m.isLeap():
                return abs(m.getMonth())
        return 0

    def getMonth(self, lunar_month):
        """
        获取农历月
        :param lunar_month: 闰月数字，1代表闰1月，0代表无闰月
        :return: 农历月
        """
        for i in range(0, len(self.__months)):
            m = self.__months[i]
            if m.getYear() == self.__year and m.getMonth() == lunar_month:
                return m
        return None

    def __getZaoByGan(self, index, name):
        offset = index - Solar.fromJulianDay(self.getMonth(1).getFirstJulianDay()).getLunar().getDayGanIndex()
        if offset < 0:
            offset += 10
        return name.replace("几", LunarUtil.NUMBER[offset + 1], 1)

    def __getZaoByZhi(self, index, name):
        offset = index - Solar.fromJulianDay(self.getMonth(1).getFirstJulianDay()).getLunar().getDayZhiIndex()
        if offset < 0:
            offset += 12
        return name.replace("几", LunarUtil.NUMBER[offset + 1], 1)

    def getTouLiang(self):
        return self.__getZaoByZhi(0, "几鼠偷粮")

    def getCaoZi(self):
        return self.__getZaoByZhi(0, "草子几分")

    def getGengTian(self):
        """
        获取耕田（正月第一个丑日是初几，就是几牛耕田）
        :return: 耕田，如：六牛耕田
        """
        return self.__getZaoByZhi(1, "几牛耕田")

    def getHuaShou(self):
        return self.__getZaoByZhi(3, "花收几分")

    def getZhiShui(self):
        """
        获取治水（正月第一个辰日是初几，就是几龙治水）
        :return: 治水，如：二龙治水
        """
        return self.__getZaoByZhi(4, "几龙治水")

    def getTuoGu(self):
        return self.__getZaoByZhi(6, "几马驮谷")

    def getQiangMi(self):
        return self.__getZaoByZhi(9, "几鸡抢米")

    def getKanCan(self):
        return self.__getZaoByZhi(9, "几姑看蚕")

    def getGongZhu(self):
        return self.__getZaoByZhi(11, "几屠共猪")

    def getJiaTian(self):
        return self.__getZaoByGan(0, "甲田几分")

    def getFenBing(self):
        """
        获取分饼（正月第一个丙日是初几，就是几人分饼）
        :return: 分饼，如：六人分饼
        """
        return self.__getZaoByGan(2, "几人分饼")

    def getDeJin(self):
        """
        获取得金（正月第一个辛日是初几，就是几日得金）
        :return: 得金，如：一日得金
        """
        return self.__getZaoByGan(7, "几日得金")

    def getRenBing(self):
        return self.__getZaoByGan(2, self.__getZaoByZhi(2, "几人几丙"))

    def getRenChu(self):
        return self.__getZaoByGan(3, self.__getZaoByZhi(2, "几人几锄"))

    def getYuan(self):
        return LunarYear.YUAN[int((self.__year + 2696) / 60) % 3] + "元"

    def getYun(self):
        return LunarYear.YUN[int((self.__year + 2696) / 20) % 9] + "运"

    def getNineStar(self):
        index = LunarUtil.getJiaZiIndex(self.getGanZhi()) + 1
        yuan = int((self.__year + 2696) / 60) % 3
        offset = (62 + yuan * 3 - index) % 9
        if 0 == offset:
            offset = 9
        return NineStar.fromIndex(offset - 1)

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

    def getPositionTaiSui(self):
        return LunarUtil.POSITION_TAI_SUI_YEAR[self.__zhiIndex]

    def getPositionTaiSuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionTaiSui()]

    def next(self, n):
        """
        获取往后推几年的阴历年，如果要往前推，则年数用负数
        :param n: 年数
        :return: 阴历年
        """
        return LunarYear.fromYear(self.__year + n)
