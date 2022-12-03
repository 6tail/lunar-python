# -*- coding: utf-8 -*-
from datetime import timedelta

from . import ExactDate, Solar, NineStar, EightChar, JieQi, ShuJiu, Fu, LunarTime
from .util import LunarUtil, SolarUtil


class Lunar:
    """
    阴历日期
    """
    JIE_QI = ("冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪")
    JIE_QI_IN_USE = ("DA_XUE", "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "DONG_ZHI", "XIAO_HAN", "DA_HAN", "LI_CHUN", "YU_SHUI", "JING_ZHE")

    def __init__(self, lunar_year, lunar_month, lunar_day, hour, minute, second):
        from . import LunarYear
        y = LunarYear.fromYear(lunar_year)
        m = y.getMonth(lunar_month)
        if m is None:
            raise Exception("wrong lunar year %d  month %d" % (lunar_year, lunar_month))
        if lunar_day < 1:
            raise Exception("lunar day must bigger than 0")
        days = m.getDayCount()
        if lunar_day > days:
            raise Exception("only %d days in lunar year %d month %d" % (days, lunar_year, lunar_month))
        self.__year = lunar_year
        self.__month = lunar_month
        self.__day = lunar_day
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__jieQi = {}
        self.__jieQiList = []
        self.__eightChar = None
        noon = Solar.fromJulianDay(m.getFirstJulianDay() + lunar_day - 1)
        self.__solar = Solar.fromYmdHms(noon.getYear(), noon.getMonth(), noon.getDay(), hour, minute, second)
        if noon.getYear() != lunar_year:
            y = LunarYear.fromYear(noon.getYear())
        self.__compute(y)

    def __compute(self, y):
        self.__computeJieQi(y)
        self.__computeYear()
        self.__computeMonth()
        self.__computeDay()
        self.__computeTime()
        self.__computeWeek()

    def __computeJieQi(self, y):
        julian_days = y.getJieQiJulianDays()
        for i in range(0, len(Lunar.JIE_QI_IN_USE)):
            name = Lunar.JIE_QI_IN_USE[i]
            self.__jieQi[name] = Solar.fromJulianDay(julian_days[i])
            self.__jieQiList.append(name)

    def __computeYear(self):
        # 以正月初一开始
        offset = self.__year - 4
        year_gan_index = offset % 10
        year_zhi_index = offset % 12

        if year_gan_index < 0:
            year_gan_index += 10

        if year_zhi_index < 0:
            year_zhi_index += 12

        # 以立春作为新一年的开始的干支纪年
        g = year_gan_index
        z = year_zhi_index

        # 精确的干支纪年，以立春交接时刻为准
        g_exact = year_gan_index
        z_exact = year_zhi_index

        solar_year = self.__solar.getYear()
        solar_ymd = self.__solar.toYmd()
        solar_ymd_hms = self.__solar.toYmdHms()

        # 获取立春的阳历时刻
        li_chun = self.__jieQi["立春"]
        if li_chun.getYear() != solar_year:
            li_chun = self.__jieQi["LI_CHUN"]
        li_chun_ymd = li_chun.toYmd()
        li_chun_ymd_hms = li_chun.toYmdHms()

        # 阳历和阴历年份相同代表正月初一及以后
        if self.__year == solar_year:
            # 立春日期判断
            if solar_ymd < li_chun_ymd:
                g -= 1
                z -= 1
            # 立春交接时刻判断
            if solar_ymd_hms < li_chun_ymd_hms:
                g_exact -= 1
                z_exact -= 1
        elif self.__year < solar_year:
            if solar_ymd >= li_chun_ymd:
                g += 1
                z += 1
            if solar_ymd_hms >= li_chun_ymd_hms:
                g_exact += 1
                z_exact += 1

        self.__yearGanIndex = year_gan_index
        self.__yearZhiIndex = year_zhi_index

        self.__yearGanIndexByLiChun = (g + 10 if g < 0 else g) % 10
        self.__yearZhiIndexByLiChun = (z + 12 if z < 0 else z) % 12

        self.__yearGanIndexExact = (g_exact + 10 if g_exact < 0 else g_exact) % 10
        self.__yearZhiIndexExact = (z_exact + 12 if z_exact < 0 else z_exact) % 12

    def __computeMonth(self):
        ymd = self.__solar.toYmd()
        time = self.__solar.toYmdHms()
        size = len(Lunar.JIE_QI_IN_USE)

        # 序号：大雪以前-3，大雪到小寒之间-2，小寒到立春之间-1，立春之后0
        index = -3
        start = None
        for i in range(0, size, 2):
            end = self.__jieQi[Lunar.JIE_QI_IN_USE[i]]
            symd = ymd if start is None else start.toYmd()
            if symd <= ymd < end.toYmd():
                break
            start = end
            index += 1
        # 干偏移值（以立春当天起算）
        g_offset = (((self.__yearGanIndexByLiChun + (1 if index < 0 else 0)) % 5 + 1) * 2) % 10
        self.__monthGanIndex = ((index + 10 if index < 0 else index) + g_offset) % 10
        self.__monthZhiIndex = ((index + 12 if index < 0 else index) + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12

        index = -3
        start = None
        for i in range(0, size, 2):
            end = self.__jieQi[Lunar.JIE_QI_IN_USE[i]]
            stime = time if start is None else start.toYmdHms()
            if stime <= time < end.toYmdHms():
                break
            start = end
            index += 1
        # 干偏移值（以立春交接时刻起算）
        g_offset = (((self.__yearGanIndexExact + (1 if index < 0 else 0)) % 5 + 1) * 2) % 10
        self.__monthGanIndexExact = ((index + 10 if index < 0 else index) + g_offset) % 10
        self.__monthZhiIndexExact = ((index + 12 if index < 0 else index) + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12

    def __computeDay(self):
        noon = Solar.fromYmdHms(self.__solar.getYear(), self.__solar.getMonth(), self.__solar.getDay(), 12, 0, 0)
        offset = int(noon.getJulianDay()) - 11
        day_gan_index = offset % 10
        day_zhi_index = offset % 12

        self.__dayGanIndex = day_gan_index
        self.__dayZhiIndex = day_zhi_index

        day_gan_exact = day_gan_index
        day_zhi_exact = day_zhi_index

        # 八字流派2，晚子时（夜子/子夜）日柱算当天
        self.__dayGanIndexExact2 = day_gan_exact
        self.__dayZhiIndexExact2 = day_zhi_exact

        # 八字流派1，晚子时（夜子/子夜）日柱算明天
        hm = ("0" if self.__hour < 10 else "") + str(self.__hour) + ":" + ("0" if self.__minute < 10 else "") + str(self.__minute)
        if "23:00" <= hm <= "23:59":
            day_gan_exact += 1
            if day_gan_exact >= 10:
                day_gan_exact -= 10
            day_zhi_exact += 1
            if day_zhi_exact >= 12:
                day_zhi_exact -= 12
        self.__dayGanIndexExact = day_gan_exact
        self.__dayZhiIndexExact = day_zhi_exact

    def __computeTime(self):
        time_zhi_index = LunarUtil.getTimeZhiIndex(("0" if self.__hour < 10 else "") + str(self.__hour) + ":" + ("0" if self.__minute < 10 else "") + str(self.__minute))
        self.__timeZhiIndex = time_zhi_index
        self.__timeGanIndex = (self.__dayGanIndexExact % 5 * 2 + time_zhi_index) % 10

    def __computeWeek(self):
        self.__weekIndex = self.__solar.getWeek()

    @staticmethod
    def fromYmdHms(lunar_year, lunar_month, lunar_day, hour, minute, second):
        return Lunar(lunar_year, lunar_month, lunar_day, hour, minute, second)

    @staticmethod
    def fromYmd(lunar_year, lunar_month, lunar_day):
        return Lunar(lunar_year, lunar_month, lunar_day, 0, 0, 0)

    @staticmethod
    def fromDate(date):
        from . import LunarYear
        year = 0
        month = 0
        day = 0
        solar = Solar.fromDate(date)
        current_year = solar.getYear()
        current_month = solar.getMonth()
        current_day = solar.getDay()
        ly = LunarYear.fromYear(current_year)
        for m in ly.getMonths():
            # 初一
            first_day = Solar.fromJulianDay(m.getFirstJulianDay())
            days = ExactDate.getDaysBetween(first_day.getYear(), first_day.getMonth(), first_day.getDay(), current_year, current_month, current_day)
            if days < m.getDayCount():
                year = m.getYear()
                month = m.getMonth()
                day = days + 1
                break
        return Lunar(year, month, day, solar.getHour(), solar.getMinute(), solar.getSecond())

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

    def getHour(self):
        return self.__hour

    def getMinute(self):
        return self.__minute

    def getSecond(self):
        return self.__second

    def getSolar(self):
        return self.__solar

    def getYearGan(self):
        return LunarUtil.GAN[self.__yearGanIndex + 1]

    def getYearGanByLiChun(self):
        return LunarUtil.GAN[self.__yearGanIndexByLiChun + 1]

    def getYearGanExact(self):
        return LunarUtil.GAN[self.__yearGanIndexExact + 1]

    def getYearZhi(self):
        return LunarUtil.ZHI[self.__yearZhiIndex + 1]

    def getYearZhiByLiChun(self):
        return LunarUtil.ZHI[self.__yearZhiIndexByLiChun + 1]

    def getYearZhiExact(self):
        return LunarUtil.ZHI[self.__yearZhiIndexExact + 1]

    def getYearInGanZhi(self):
        return self.getYearGan() + self.getYearZhi()

    def getYearInGanZhiByLiChun(self):
        return self.getYearGanByLiChun() + self.getYearZhiByLiChun()

    def getYearInGanZhiExact(self):
        return self.getYearGanExact() + self.getYearZhiExact()

    def getMonthGan(self):
        return LunarUtil.GAN[self.__monthGanIndex + 1]

    def getMonthGanExact(self):
        return LunarUtil.GAN[self.__monthGanIndexExact + 1]

    def getMonthZhi(self):
        return LunarUtil.ZHI[self.__monthZhiIndex + 1]

    def getMonthZhiExact(self):
        return LunarUtil.ZHI[self.__monthZhiIndexExact + 1]

    def getMonthInGanZhi(self):
        return self.getMonthGan() + self.getMonthZhi()

    def getMonthInGanZhiExact(self):
        return self.getMonthGanExact() + self.getMonthZhiExact()

    def getDayGan(self):
        return LunarUtil.GAN[self.__dayGanIndex + 1]

    def getDayGanExact(self):
        return LunarUtil.GAN[self.__dayGanIndexExact + 1]

    def getDayGanExact2(self):
        return LunarUtil.GAN[self.__dayGanIndexExact2 + 1]

    def getDayZhi(self):
        return LunarUtil.ZHI[self.__dayZhiIndex + 1]

    def getDayZhiExact(self):
        return LunarUtil.ZHI[self.__dayZhiIndexExact + 1]

    def getDayZhiExact2(self):
        return LunarUtil.ZHI[self.__dayZhiIndexExact2 + 1]

    def getDayInGanZhi(self):
        return self.getDayGan() + self.getDayZhi()

    def getDayInGanZhiExact(self):
        return self.getDayGanExact() + self.getDayZhiExact()

    def getDayInGanZhiExact2(self):
        return self.getDayGanExact2() + self.getDayZhiExact2()

    def getTimeGan(self):
        return LunarUtil.GAN[self.__timeGanIndex + 1]

    def getTimeZhi(self):
        return LunarUtil.ZHI[self.__timeZhiIndex + 1]

    def getTimeInGanZhi(self):
        return self.getTimeGan() + self.getTimeZhi()

    def getYearShengXiao(self):
        return LunarUtil.SHENGXIAO[self.__yearZhiIndex + 1]

    def getYearShengXiaoByLiChun(self):
        return LunarUtil.SHENGXIAO[self.__yearZhiIndexByLiChun + 1]

    def getYearShengXiaoExact(self):
        return LunarUtil.SHENGXIAO[self.__yearZhiIndexExact + 1]

    def getMonthShengXiao(self):
        return LunarUtil.SHENGXIAO[self.__monthZhiIndex + 1]

    def getMonthShengXiaoExact(self):
        return LunarUtil.SHENGXIAO[self.__monthZhiIndexExact + 1]

    def getDayShengXiao(self):
        return LunarUtil.SHENGXIAO[self.__dayZhiIndex + 1]

    def getTimeShengXiao(self):
        return LunarUtil.SHENGXIAO[self.__timeZhiIndex + 1]

    def getYearInChinese(self):
        y = str(self.__year)
        s = ""
        for i in range(0, len(y)):
            s += LunarUtil.NUMBER[ord(y[i]) - 48]
        return s

    def getMonthInChinese(self):
        month = self.__month
        return ("闰" if month < 0 else "") + LunarUtil.MONTH[abs(month)]

    def getDayInChinese(self):
        return LunarUtil.DAY[self.__day]

    def getPengZuGan(self):
        return LunarUtil.PENG_ZU_GAN[self.__dayGanIndex + 1]

    def getPengZuZhi(self):
        return LunarUtil.PENG_ZU_ZHI[self.__dayZhiIndex + 1]

    def getPositionXi(self):
        return self.getDayPositionXi()

    def getPositionXiDesc(self):
        return self.getDayPositionXiDesc()

    def getPositionYangGui(self):
        return self.getDayPositionYangGui()

    def getPositionYangGuiDesc(self):
        return self.getDayPositionYangGuiDesc()

    def getPositionYinGui(self):
        return self.getDayPositionYinGui()

    def getPositionYinGuiDesc(self):
        return self.getDayPositionYinGuiDesc()

    def getPositionFu(self):
        return self.getDayPositionFu()

    def getPositionFuDesc(self):
        return self.getDayPositionFuDesc()

    def getPositionCai(self):
        return self.getDayPositionCai()

    def getPositionCaiDesc(self):
        return self.getDayPositionCaiDesc()

    def getDayPositionXi(self):
        return LunarUtil.POSITION_XI[self.__dayGanIndex + 1]

    def getDayPositionXiDesc(self):
        return LunarUtil.POSITION_DESC[self.getDayPositionXi()]

    def getDayPositionYangGui(self):
        return LunarUtil.POSITION_YANG_GUI[self.__dayGanIndex + 1]

    def getDayPositionYangGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getDayPositionYangGui()]

    def getDayPositionYinGui(self):
        return LunarUtil.POSITION_YIN_GUI[self.__dayGanIndex + 1]

    def getDayPositionYinGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getDayPositionYinGui()]

    def getDayPositionFu(self, sect=2):
        return (LunarUtil.POSITION_FU if 1 == sect else LunarUtil.POSITION_FU_2)[self.__dayGanIndex + 1]

    def getDayPositionFuDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getDayPositionFu(sect)]

    def getDayPositionCai(self):
        return LunarUtil.POSITION_CAI[self.__dayGanIndex + 1]

    def getDayPositionCaiDesc(self):
        return LunarUtil.POSITION_DESC[self.getDayPositionCai()]

    def getYearPositionTaiSui(self, sect=2):
        if 1 == sect:
            year_zhi_index = self.__yearZhiIndex
        elif 3 == sect:
            year_zhi_index = self.__yearZhiIndexExact
        else:
            year_zhi_index = self.__yearZhiIndexByLiChun
        return LunarUtil.POSITION_TAI_SUI_YEAR[year_zhi_index]

    def getYearPositionTaiSuiDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getYearPositionTaiSui(sect)]

    def __getMonthPositionTaiSui(self, month_zhi_index, month_gan_index):
        m = month_zhi_index - LunarUtil.BASE_MONTH_ZHI_INDEX
        if m < 0:
            m += 12
        m = m % 4
        if 0 == m:
            p = "艮"
        elif 2 == m:
            p = "坤"
        elif 3 == m:
            p = "巽"
        else:
            p = LunarUtil.POSITION_GAN[month_gan_index]
        return p

    def getMonthPositionTaiSui(self, sect=2):
        if 3 == sect:
            month_zhi_index = self.__monthZhiIndexExact
            month_gan_index = self.__monthGanIndexExact
        else:
            month_zhi_index = self.__monthZhiIndex
            month_gan_index = self.__monthGanIndex
        return self.__getMonthPositionTaiSui(month_zhi_index, month_gan_index)

    def getMonthPositionTaiSuiDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getMonthPositionTaiSui(sect)]

    def __getDayPositionTaiSui(self, day_in_gan_zhi, year_zhi_index):
        if day_in_gan_zhi in "甲子,乙丑,丙寅,丁卯,戊辰,已巳":
            p = "震"
        elif day_in_gan_zhi in "丙子,丁丑,戊寅,已卯,庚辰,辛巳":
            p = "离"
        elif day_in_gan_zhi in "戊子,已丑,庚寅,辛卯,壬辰,癸巳":
            p = "中"
        elif day_in_gan_zhi in "庚子,辛丑,壬寅,癸卯,甲辰,乙巳":
            p = "兑"
        elif day_in_gan_zhi in "壬子,癸丑,甲寅,乙卯,丙辰,丁巳":
            p = "坎"
        else:
            p = LunarUtil.POSITION_TAI_SUI_YEAR[year_zhi_index]
        return p

    def getDayPositionTaiSui(self, sect=2):
        if 1 == sect:
            day_in_gan_zhi = self.getDayInGanZhi()
            year_zhi_index = self.__yearZhiIndex
        elif 3 == sect:
            day_in_gan_zhi = self.getDayInGanZhi()
            year_zhi_index = self.__yearZhiIndexExact
        else:
            day_in_gan_zhi = self.getDayInGanZhiExact2()
            year_zhi_index = self.__yearZhiIndexByLiChun
        return self.__getDayPositionTaiSui(day_in_gan_zhi, year_zhi_index)

    def getDayPositionTaiSuiDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getDayPositionTaiSui(sect)]

    def getTimePositionXi(self):
        return LunarUtil.POSITION_XI[self.__timeGanIndex + 1]

    def getTimePositionXiDesc(self):
        return LunarUtil.POSITION_DESC[self.getTimePositionXi()]

    def getTimePositionYangGui(self):
        return LunarUtil.POSITION_YANG_GUI[self.__timeGanIndex + 1]

    def getTimePositionYangGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getTimePositionYangGui()]

    def getTimePositionYinGui(self):
        return LunarUtil.POSITION_YIN_GUI[self.__timeGanIndex + 1]

    def getTimePositionYinGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getTimePositionYinGui()]

    def getTimePositionFu(self, sect=2):
        return (LunarUtil.POSITION_FU if 1 == sect else LunarUtil.POSITION_FU_2)[self.__timeGanIndex + 1]

    def getTimePositionFuDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getTimePositionFu(sect)]

    def getTimePositionCai(self):
        return LunarUtil.POSITION_CAI[self.__timeGanIndex + 1]

    def getTimePositionCaiDesc(self):
        return LunarUtil.POSITION_DESC[self.getTimePositionCai()]

    def getChong(self):
        return self.getDayChong()

    def getDayChong(self):
        return LunarUtil.CHONG[self.__dayZhiIndex]

    def getTimeChong(self):
        return LunarUtil.CHONG[self.__timeZhiIndex]

    def getChongGan(self):
        return self.getDayChongGan()

    def getDayChongGan(self):
        return LunarUtil.CHONG_GAN[self.__dayGanIndex]

    def getTimeChongGan(self):
        return LunarUtil.CHONG_GAN[self.__timeGanIndex]

    def getChongGanTie(self):
        return self.getDayChongGanTie()

    def getDayChongGanTie(self):
        return LunarUtil.CHONG_GAN_TIE[self.__dayGanIndex]

    def getTimeChongGanTie(self):
        return LunarUtil.CHONG_GAN_TIE[self.__timeGanIndex]

    def getChongShengXiao(self):
        return self.getDayChongShengXiao()

    def getDayChongShengXiao(self):
        chong = self.getDayChong()
        for i in range(0, len(LunarUtil.ZHI)):
            if LunarUtil.ZHI[i] == chong:
                return LunarUtil.SHENGXIAO[i]
        return ""

    def getTimeChongShengXiao(self):
        chong = self.getTimeChong()
        for i in range(0, len(LunarUtil.ZHI)):
            if LunarUtil.ZHI[i] == chong:
                return LunarUtil.SHENGXIAO[i]
        return ""

    def getChongDesc(self):
        return self.getDayChongDesc()

    def getDayChongDesc(self):
        return "(" + self.getDayChongGan() + self.getDayChong() + ")" + self.getDayChongShengXiao()

    def getTimeChongDesc(self):
        return "(" + self.getTimeChongGan() + self.getTimeChong() + ")" + self.getTimeChongShengXiao()

    def getSha(self):
        return self.getDaySha()

    def getDaySha(self):
        return LunarUtil.SHA[self.getDayZhi()]

    def getTimeSha(self):
        return LunarUtil.SHA[self.getTimeZhi()]

    def getYearNaYin(self):
        return LunarUtil.NAYIN[self.getYearInGanZhi()]

    def getMonthNaYin(self):
        return LunarUtil.NAYIN[self.getMonthInGanZhi()]

    def getDayNaYin(self):
        return LunarUtil.NAYIN[self.getDayInGanZhi()]

    def getTimeNaYin(self):
        return LunarUtil.NAYIN[self.getTimeInGanZhi()]

    def getSeason(self):
        return LunarUtil.SEASON[abs(self.__month)]

    @staticmethod
    def __convertJieQi(name):
        jq = name
        if "DONG_ZHI" == jq:
            jq = "冬至"
        elif "DA_HAN" == jq:
            jq = "大寒"
        elif "XIAO_HAN" == jq:
            jq = "小寒"
        elif "LI_CHUN" == jq:
            jq = "立春"
        elif "DA_XUE" == jq:
            jq = "大雪"
        elif "YU_SHUI" == jq:
            jq = "雨水"
        elif "JING_ZHE" == jq:
            jq = "惊蛰"
        return jq

    def getJie(self):
        for i in range(0, len(Lunar.JIE_QI_IN_USE), 2):
            key = Lunar.JIE_QI_IN_USE[i]
            d = self.__jieQi[key]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return self.__convertJieQi(key)
        return ""

    def getQi(self):
        for i in range(1, len(Lunar.JIE_QI_IN_USE), 2):
            key = Lunar.JIE_QI_IN_USE[i]
            d = self.__jieQi[key]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return self.__convertJieQi(key)
        return ""

    def getWeek(self):
        return self.__weekIndex

    def getWeekInChinese(self):
        return SolarUtil.WEEK[self.getWeek()]

    def getXiu(self):
        return LunarUtil.XIU[self.getDayZhi() + str(self.getWeek())]

    def getXiuLuck(self):
        return LunarUtil.XIU_LUCK[self.getXiu()]

    def getXiuSong(self):
        return LunarUtil.XIU_SONG[self.getXiu()]

    def getZheng(self):
        return LunarUtil.ZHENG[self.getXiu()]

    def getAnimal(self):
        return LunarUtil.ANIMAL[self.getXiu()]

    def getGong(self):
        return LunarUtil.GONG[self.getXiu()]

    def getShou(self):
        return LunarUtil.SHOU[self.getGong()]

    def getFestivals(self):
        fs = []
        md = "%d-%d" % (self.__month, self.__day)
        if md in LunarUtil.FESTIVAL:
            fs.append(LunarUtil.FESTIVAL[md])
        if abs(self.__month) == 12 and self.__day >= 29 and self.__year != self.next(1).getYear():
            fs.append("除夕")
        return fs

    def getOtherFestivals(self):
        arr = []
        md = "%d-%d" % (self.__month, self.__day)
        if md in LunarUtil.OTHER_FESTIVAL:
            fs = LunarUtil.OTHER_FESTIVAL[md]
            for f in fs:
                arr.append(f)
        solar_ymd = self.__solar.toYmd()
        if solar_ymd == self.__jieQi["清明"].next(-1).toYmd():
            arr.append("寒食节")

        jq = self.__jieQi["立春"]
        offset = 4 - jq.getLunar().getDayGanIndex()
        if offset < 0:
            offset += 10
        if solar_ymd == jq.next(offset + 40).toYmd():
            arr.append("春社")

        jq = self.__jieQi["立秋"]
        offset = 4 - jq.getLunar().getDayGanIndex()
        if offset < 0:
            offset += 10
        if solar_ymd == jq.next(offset + 40).toYmd():
            arr.append("秋社")
        return arr

    def getEightChar(self):
        if self.__eightChar is None:
            self.__eightChar = EightChar.fromLunar(self)
        return self.__eightChar

    def getBaZi(self):
        ba_zi = self.getEightChar()
        return [ba_zi.getYear(), ba_zi.getMonth(), ba_zi.getDay(), ba_zi.getTime()]

    def getBaZiWuXing(self):
        ba_zi = self.getEightChar()
        return [ba_zi.getYearWuXing(), ba_zi.getMonthWuXing(), ba_zi.getDayWuXing(), ba_zi.getTimeWuXing()]

    def getBaZiNaYin(self):
        ba_zi = self.getEightChar()
        return [ba_zi.getYearNaYin(), ba_zi.getMonthNaYin(), ba_zi.getDayNaYin(), ba_zi.getTimeNaYin()]

    def getBaZiShiShenGan(self):
        ba_zi = self.getEightChar()
        return [ba_zi.getYearShiShenGan(), ba_zi.getMonthShiShenGan(), ba_zi.getDayShiShenGan(), ba_zi.getTimeShiShenGan()]

    def getBaZiShiShenZhi(self):
        ba_zi = self.getEightChar()
        return [ba_zi.getYearShiShenZhi()[0], ba_zi.getMonthShiShenZhi()[0], ba_zi.getDayShiShenZhi()[0], ba_zi.getTimeShiShenZhi()[0]]

    def getBaZiShiShenYearZhi(self):
        return self.getEightChar().getYearShiShenZhi()

    def getBaZiShiShenMonthZhi(self):
        return self.getEightChar().getMonthShiShenZhi()

    def getBaZiShiShenDayZhi(self):
        return self.getEightChar().getDayShiShenZhi()

    def getBaZiShiShenTimeZhi(self):
        return self.getEightChar().getTimeShiShenZhi()

    def getZhiXing(self):
        offset = self.__dayZhiIndex - self.__monthZhiIndex
        if offset < 0:
            offset += 12
        return LunarUtil.ZHI_XING[offset + 1]

    def getDayTianShen(self):
        offset = LunarUtil.ZHI_TIAN_SHEN_OFFSET[self.getMonthZhi()]
        return LunarUtil.TIAN_SHEN[(self.__dayZhiIndex + offset) % 12 + 1]

    def getTimeTianShen(self):
        offset = LunarUtil.ZHI_TIAN_SHEN_OFFSET[self.getDayZhiExact()]
        return LunarUtil.TIAN_SHEN[(self.__timeZhiIndex + offset) % 12 + 1]

    def getDayTianShenType(self):
        return LunarUtil.TIAN_SHEN_TYPE[self.getDayTianShen()]

    def getTimeTianShenType(self):
        return LunarUtil.TIAN_SHEN_TYPE[self.getTimeTianShen()]

    def getDayTianShenLuck(self):
        return LunarUtil.TIAN_SHEN_TYPE_LUCK[self.getDayTianShenType()]

    def getTimeTianShenLuck(self):
        return LunarUtil.TIAN_SHEN_TYPE_LUCK[self.getTimeTianShenType()]

    def getDayPositionTai(self):
        return LunarUtil.POSITION_TAI_DAY[LunarUtil.getJiaZiIndex(self.getDayInGanZhi())]

    def getMonthPositionTai(self):
        m = self.__month
        if m < 0:
            return ""
        return LunarUtil.POSITION_TAI_MONTH[m - 1]

    def getDayYi(self, sect=2):
        """
        获取每日宜
        :return: 宜
        """
        if 2 == sect:
            month_gan_zhi = self.getMonthInGanZhiExact()
        else:
            month_gan_zhi = self.getMonthInGanZhi()
        return LunarUtil.getDayYi(month_gan_zhi, self.getDayInGanZhi())

    def getDayJi(self, sect=2):
        """
        获取每日忌
        :return: 忌
        """
        if 2 == sect:
            month_gan_zhi = self.getMonthInGanZhiExact()
        else:
            month_gan_zhi = self.getMonthInGanZhi()
        return LunarUtil.getDayJi(month_gan_zhi, self.getDayInGanZhi())

    def getTimeYi(self):
        """
        获取时宜
        :return: 宜
        """
        return LunarUtil.getTimeYi(self.getDayInGanZhiExact(), self.getTimeInGanZhi())

    def getTimeJi(self):
        """
        获取时忌
        :return: 忌
        """
        return LunarUtil.getTimeJi(self.getDayInGanZhiExact(), self.getTimeInGanZhi())

    def getDayJiShen(self):
        """
        获取日吉神（宜趋）
        :return: 日吉神
        """
        return LunarUtil.getDayJiShen(self.getMonth(), self.getDayInGanZhi())

    def getDayXiongSha(self):
        """
        获取日凶煞（宜忌）
        :return: 日凶煞
        """
        return LunarUtil.getDayXiongSha(self.getMonth(), self.getDayInGanZhi())

    def getYueXiang(self):
        """
        获取月相
        :return: 月相
        """
        return LunarUtil.YUE_XIANG[self.__day]

    def __getYearNineStar(self, year_in_gan_zhi):
        index_exact = LunarUtil.getJiaZiIndex(year_in_gan_zhi) + 1
        index = LunarUtil.getJiaZiIndex(self.getYearInGanZhi()) + 1
        year_offset = index_exact - index
        if year_offset > 1:
            year_offset -= 60
        elif year_offset < -1:
            year_offset += 60
        yuan = int((self.__year + year_offset + 2696) / 60) % 3
        offset = (62 + yuan * 3 - index_exact) % 9
        if 0 == offset:
            offset = 9
        return NineStar.fromIndex(offset - 1)

    def getYearNineStar(self, sect=2):
        if 1 == sect:
            year_in_gan_zhi = self.getYearInGanZhi()
        elif 3 == sect:
            year_in_gan_zhi = self.getYearInGanZhiExact()
        else:
            year_in_gan_zhi = self.getYearInGanZhiByLiChun()
        return self.__getYearNineStar(year_in_gan_zhi)

    @staticmethod
    def __getMonthNineStar(year_zhi_index, month_zhi_index):
        index = year_zhi_index % 3
        n = 27 - index * 3
        if month_zhi_index < LunarUtil.BASE_MONTH_ZHI_INDEX:
            n -= 3
        offset = (n - month_zhi_index) % 9
        return NineStar.fromIndex(offset)

    def getMonthNineStar(self, sect=2):
        if 1 == sect:
            year_zhi_index = self.__yearZhiIndex
            month_zhi_index = self.__monthZhiIndex
        elif 3 == sect:
            year_zhi_index = self.__yearZhiIndexExact
            month_zhi_index = self.__monthZhiIndexExact
        else:
            year_zhi_index = self.__yearZhiIndexByLiChun
            month_zhi_index = self.__monthZhiIndex
        return self.__getMonthNineStar(year_zhi_index, month_zhi_index)

    def getDayNineStar(self):
        solar_ymd = self.__solar.toYmd()
        dong_zhi = self.__jieQi["冬至"]
        dong_zhi2 = self.__jieQi["DONG_ZHI"]
        xia_zhi = self.__jieQi["夏至"]

        dong_zhi_index = LunarUtil.getJiaZiIndex(dong_zhi.getLunar().getDayInGanZhi())
        dong_zhi_index2 = LunarUtil.getJiaZiIndex(dong_zhi2.getLunar().getDayInGanZhi())
        xia_zhi_index = LunarUtil.getJiaZiIndex(xia_zhi.getLunar().getDayInGanZhi())

        if dong_zhi_index > 29:
            solar_shun_bai = dong_zhi.next(60 - dong_zhi_index)
        else:
            solar_shun_bai = dong_zhi.next(-dong_zhi_index)
        solar_shun_bai_ymd = solar_shun_bai.toYmd()
        if dong_zhi_index2 > 29:
            solar_shun_bai2 = dong_zhi2.next(60 - dong_zhi_index2)
        else:
            solar_shun_bai2 = dong_zhi2.next(-dong_zhi_index2)
        solar_shun_bai_ymd2 = solar_shun_bai2.toYmd()
        if xia_zhi_index > 29:
            solar_ni_zi = xia_zhi.next(60 - xia_zhi_index)
        else:
            solar_ni_zi = xia_zhi.next(-xia_zhi_index)
        solar_ni_zi_ymd = solar_ni_zi.toYmd()
        offset = 0
        if solar_shun_bai_ymd <= solar_ymd < solar_ni_zi_ymd:
            offset = ExactDate.getDaysBetweenDate(solar_shun_bai.getCalendar(), self.__solar.getCalendar()) % 9
        elif solar_ni_zi_ymd <= solar_ymd < solar_shun_bai_ymd2:
            offset = 8 - (ExactDate.getDaysBetweenDate(solar_ni_zi.getCalendar(), self.__solar.getCalendar()) % 9)
        elif solar_ymd >= solar_shun_bai_ymd2:
            offset = ExactDate.getDaysBetweenDate(solar_shun_bai2.getCalendar(), self.__solar.getCalendar()) % 9
        elif solar_ymd < solar_shun_bai_ymd:
            offset = (8 + ExactDate.getDaysBetweenDate(self.__solar.getCalendar(), solar_shun_bai.getCalendar())) % 9
        return NineStar.fromIndex(offset)

    def getTimeNineStar(self):
        solar_ymd = self.__solar.toYmd()
        asc = False
        if self.__jieQi["冬至"].toYmd() <= solar_ymd < self.__jieQi["夏至"].toYmd():
            asc = True
        elif solar_ymd >= self.__jieQi["DONG_ZHI"].toYmd():
            asc = True
        start = 6 if asc else 2
        day_zhi = self.getDayZhi()
        if day_zhi in "子午卯酉":
            start = 0 if asc else 8
        elif day_zhi in "辰戌丑未":
            start = 3 if asc else 5
        index = start + self.__timeZhiIndex if asc else start + 9 - self.__timeZhiIndex
        return NineStar.fromIndex(index % 9)

    def getJieQiTable(self):
        return self.__jieQi

    def getJieQiList(self):
        return self.__jieQiList

    def getTimeGanIndex(self):
        return self.__timeGanIndex

    def getTimeZhiIndex(self):
        return self.__timeZhiIndex

    def getDayGanIndex(self):
        return self.__dayGanIndex

    def getDayZhiIndex(self):
        return self.__dayZhiIndex

    def getDayGanIndexExact(self):
        return self.__dayGanIndexExact

    def getDayGanIndexExact2(self):
        return self.__dayGanIndexExact2

    def getDayZhiIndexExact(self):
        return self.__dayZhiIndexExact

    def getDayZhiIndexExact2(self):
        return self.__dayZhiIndexExact2

    def getMonthGanIndex(self):
        return self.__monthGanIndex

    def getMonthZhiIndex(self):
        return self.__monthZhiIndex

    def getMonthGanIndexExact(self):
        return self.__monthGanIndexExact

    def getMonthZhiIndexExact(self):
        return self.__monthZhiIndexExact

    def getYearGanIndex(self):
        return self.__yearGanIndex

    def getYearZhiIndex(self):
        return self.__yearZhiIndex

    def getYearGanIndexByLiChun(self):
        return self.__yearGanIndexByLiChun

    def getYearZhiIndexByLiChun(self):
        return self.__yearZhiIndexByLiChun

    def getYearGanIndexExact(self):
        return self.__yearGanIndexExact

    def getYearZhiIndexExact(self):
        return self.__yearZhiIndexExact

    def getNextJie(self, whole_day=False):
        """
        获取下一节（顺推的第一个节）
        :param whole_day: 是否按天计
        :return: 节气
        """
        conditions = []
        for i in range(0, int(len(Lunar.JIE_QI_IN_USE) / 2)):
            conditions.append(Lunar.JIE_QI_IN_USE[i * 2])
        return self.__getNearJieQi(True, conditions, whole_day)

    def getPrevJie(self, whole_day=False):
        """
        获取上一节（逆推的第一个节）
        :param whole_day: 是否按天计
        :return: 节气
        """
        conditions = []
        for i in range(0, int(len(Lunar.JIE_QI_IN_USE) / 2)):
            conditions.append(Lunar.JIE_QI_IN_USE[i * 2])
        return self.__getNearJieQi(False, conditions, whole_day)

    def getNextQi(self, whole_day=False):
        """
        获取下一气令（顺推的第一个气令）
        :param whole_day: 是否按天计
        :return: 节气
        """
        conditions = []
        for i in range(0, int(len(Lunar.JIE_QI_IN_USE) / 2)):
            conditions.append(Lunar.JIE_QI_IN_USE[i * 2 + 1])
        return self.__getNearJieQi(True, conditions, whole_day)

    def getPrevQi(self, whole_day=False):
        """
        获取上一气令（逆推的第一个气令）
        :param whole_day: 是否按天计
        :return: 节气
        """
        conditions = []
        for i in range(0, int(len(Lunar.JIE_QI_IN_USE) / 2)):
            conditions.append(Lunar.JIE_QI_IN_USE[i * 2 + 1])
        return self.__getNearJieQi(False, conditions, whole_day)

    def getNextJieQi(self, whole_day=False):
        """
        获取下一节气（顺推的第一个节气）
        :param whole_day: 是否按天计
        :return: 节气
        """
        return self.__getNearJieQi(True, None, whole_day)

    def getPrevJieQi(self, whole_day=False):
        """
        获取上一节气（逆推的第一个节气）
        :param whole_day: 是否按天计
        :return: 节气
        """
        return self.__getNearJieQi(False, None, whole_day)

    def __getNearJieQi(self, forward, conditions, whole_day):
        """
        获取最近的节气，如果未找到匹配的，返回null
        :param forward: 是否顺推，true为顺推，false为逆推
        :param conditions: 过滤条件，如果设置过滤条件，仅返回匹配该名称的
        :param whole_day: 是否按天计
        :return: 节气
        """
        name = None
        near = None
        filters = set()
        if conditions is not None:
            for cond in conditions:
                filters.add(cond)
        is_filter = len(filters) > 0
        today = self.__solar.toYmd() if whole_day else self.__solar.toYmdHms()
        for key in self.JIE_QI_IN_USE:
            jq = self.__convertJieQi(key)
            if is_filter and not filters.__contains__(jq):
                continue
            solar = self.__jieQi[key]
            day = solar.toYmd() if whole_day else solar.toYmdHms()
            if forward:
                if day < today:
                    continue
                if near is None:
                    name = jq
                    near = solar
                else:
                    near_day = near.toYmd() if whole_day else near.toYmdHms()
                    if day < near_day:
                        name = jq
                        near = solar
            else:
                if day > today:
                    continue
                if near is None:
                    name = jq
                    near = solar
                else:
                    near_day = near.toYmd() if whole_day else near.toYmdHms()
                    if day > near_day:
                        name = jq
                        near = solar
        if near is None:
            return None
        return JieQi(name, near)

    def getJieQi(self):
        """
        获取节气名称，如果无节气，返回空字符串
        :return: 节气名称
        """
        for key in self.__jieQi:
            d = self.__jieQi[key]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return self.__convertJieQi(key)
        return ""

    def getCurrentJieQi(self):
        """
        获取当天节气对象，如果无节气，返回None
        :return: 节气对象
        """
        for key in self.__jieQi:
            d = self.__jieQi[key]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return JieQi(self.__convertJieQi(key), self.__solar)
        return None

    def getCurrentJie(self):
        """
        获取当天节令对象，如果无节令，返回None
        :return: 节气对象
        """
        for i in range(0, len(Lunar.JIE_QI_IN_USE), 2):
            key = Lunar.JIE_QI_IN_USE[i]
            d = self.__jieQi[key]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return JieQi(self.__convertJieQi(key), d)
        return None

    def getCurrentQi(self):
        """
        获取当天气令对象，如果无气令，返回None
        :return: 节气对象
        """
        for i in range(1, len(Lunar.JIE_QI_IN_USE), 2):
            key = Lunar.JIE_QI_IN_USE[i]
            d = self.__jieQi[key]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return JieQi(self.__convertJieQi(key), d)
        return None

    def next(self, days):
        """
        获取往后推几天的农历日期，如果要往前推，则天数用负数
        :param days: 天数
        :return: 农历日期
        """
        return self.__solar.next(days).getLunar()

    def __str__(self):
        return self.toString()

    def toString(self):
        return "%s年%s月%s" % (self.getYearInChinese(), self.getMonthInChinese(), self.getDayInChinese())

    def toFullString(self):
        s = self.toString()
        s += " " + self.getYearInGanZhi() + "(" + self.getYearShengXiao() + ")年"
        s += " " + self.getMonthInGanZhi() + "(" + self.getMonthShengXiao() + ")月"
        s += " " + self.getDayInGanZhi() + "(" + self.getDayShengXiao() + ")日"
        s += " " + self.getTimeZhi() + "(" + self.getTimeShengXiao() + ")时"
        s += " 纳音[" + self.getYearNaYin() + " " + self.getMonthNaYin() + " " + self.getDayNaYin() + " " + self.getTimeNaYin() + "]"
        s += " 星期" + self.getWeekInChinese()
        for f in self.getFestivals():
            s += " (" + f + ")"
        for f in self.getOtherFestivals():
            s += " (" + f + ")"
        jq = self.getJieQi()
        if len(jq) > 0:
            s += " [" + jq + "]"
        s += " " + self.getGong() + "方" + self.getShou()
        s += " 星宿[" + self.getXiu() + self.getZheng() + self.getAnimal() + "](" + self.getXiuLuck() + ")"
        s += " 彭祖百忌[" + self.getPengZuGan() + " " + self.getPengZuZhi() + "]"
        s += " 喜神方位[" + self.getDayPositionXi() + "](" + self.getDayPositionXiDesc() + ")"
        s += " 阳贵神方位[" + self.getDayPositionYangGui() + "](" + self.getDayPositionYangGuiDesc() + ")"
        s += " 阴贵神方位[" + self.getDayPositionYinGui() + "](" + self.getDayPositionYinGuiDesc() + ")"
        s += " 福神方位[" + self.getDayPositionFu() + "](" + self.getDayPositionFuDesc() + ")"
        s += " 财神方位[" + self.getDayPositionCai() + "](" + self.getDayPositionCaiDesc() + ")"
        s += " 冲[" + self.getChongDesc() + "]"
        s += " 煞[" + self.getSha() + "]"
        return s

    def getYearXun(self):
        """
        获取年所在旬（以正月初一作为新年的开始）
        :return: 旬
        """
        return LunarUtil.getXun(self.getYearInGanZhi())

    def getYearXunByLiChun(self):
        """
        获取年所在旬（以立春当天作为新年的开始）
        :return: 旬
        """
        return LunarUtil.getXun(self.getYearInGanZhiByLiChun())

    def getYearXunExact(self):
        """
        获取年所在旬（以立春交接时刻作为新年的开始）
        :return: 旬
        """
        return LunarUtil.getXun(self.getYearInGanZhiExact())

    def getYearXunKong(self):
        """
        获取值年空亡（以正月初一作为新年的开始）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getYearInGanZhi())

    def getYearXunKongByLiChun(self):
        """
        获取值年空亡（以立春当天作为新年的开始）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getYearInGanZhiByLiChun())

    def getYearXunKongExact(self):
        """
        获取值年空亡（以立春交接时刻作为新年的开始）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getYearInGanZhiExact())

    def getMonthXun(self):
        """
        获取月所在旬（以节交接当天起算）
        :return: 旬
        """
        return LunarUtil.getXun(self.getMonthInGanZhi())

    def getMonthXunExact(self):
        """
        获取月所在旬（以节交接时刻起算）
        :return: 旬
        """
        return LunarUtil.getXun(self.getMonthInGanZhiExact())

    def getMonthXunKong(self):
        """
        获取值月空亡（以节交接当天起算）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getMonthInGanZhi())

    def getMonthXunKongExact(self):
        """
        获取值月空亡（以节交接时刻起算）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getMonthInGanZhiExact())

    def getDayXun(self):
        """
        获取日所在旬（以节交接当天起算）
        :return: 旬
        """
        return LunarUtil.getXun(self.getDayInGanZhi())

    def getDayXunExact(self):
        """
        获取日所在旬（晚子时日柱算明天）
        :return: 旬
        """
        return LunarUtil.getXun(self.getDayInGanZhiExact())

    def getDayXunExact2(self):
        """
        获取日所在旬（晚子时日柱算当天）
        :return: 旬
        """
        return LunarUtil.getXun(self.getDayInGanZhiExact2())

    def getDayXunKong(self):
        """
        获取值日空亡
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getDayInGanZhi())

    def getDayXunKongExact(self):
        """
        获取值日空亡（晚子时日柱算明天）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getDayInGanZhiExact())

    def getDayXunKongExact2(self):
        """
        获取值日空亡（晚子时日柱算当天）
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getDayInGanZhiExact2())

    def getTimeXun(self):
        """
        获取时辰所在旬
        :return: 旬
        """
        return LunarUtil.getXun(self.getTimeInGanZhi())

    def getTimeXunKong(self):
        """
        获取值时空亡
        :return: 空亡(旬空)
        """
        return LunarUtil.getXunKong(self.getTimeInGanZhi())

    def getShuJiu(self):
        """
        获取数九
        :return: 数九，如果不是数九天，返回None
        """
        current_calendar = ExactDate.fromYmd(self.__solar.getYear(), self.__solar.getMonth(), self.__solar.getDay())
        start = self.__jieQi["DONG_ZHI"]
        start_calendar = ExactDate.fromYmd(start.getYear(), start.getMonth(), start.getDay())
        if current_calendar < start_calendar:
            start = self.__jieQi["冬至"]
            start_calendar = ExactDate.fromYmd(start.getYear(), start.getMonth(), start.getDay())
        end_calendar = start_calendar + timedelta(days=81)
        if current_calendar < start_calendar or current_calendar >= end_calendar:
            return None
        days = ExactDate.getDaysBetweenDate(start_calendar, current_calendar)
        return ShuJiu(LunarUtil.NUMBER[int(days / 9) + 1] + "九", days % 9 + 1)

    def getFu(self):
        """
        获取三伏
        :return: 三伏，如果不是伏天，返回None
        """
        current_calendar = ExactDate.fromYmd(self.__solar.getYear(), self.__solar.getMonth(), self.__solar.getDay())
        xia_zhi = self.__jieQi["夏至"]
        li_qiu = self.__jieQi["立秋"]
        start_calendar = ExactDate.fromYmd(xia_zhi.getYear(), xia_zhi.getMonth(), xia_zhi.getDay())
        add = 6 - xia_zhi.getLunar().getDayGanIndex()
        if add < 0:
            add += 10
        add += 20
        start_calendar = start_calendar + timedelta(days=add)
        if current_calendar < start_calendar:
            return None
        days = ExactDate.getDaysBetweenDate(start_calendar, current_calendar)
        if days < 10:
            return Fu("初伏", days + 1)
        start_calendar = start_calendar + timedelta(days=10)
        days = ExactDate.getDaysBetweenDate(start_calendar, current_calendar)
        if days < 10:
            return Fu("中伏", days + 1)
        start_calendar = start_calendar + timedelta(days=10)
        days = ExactDate.getDaysBetweenDate(start_calendar, current_calendar)
        li_qiu_calendar = ExactDate.fromYmd(li_qiu.getYear(), li_qiu.getMonth(), li_qiu.getDay())
        if li_qiu_calendar <= start_calendar:
            if days < 10:
                return Fu("末伏", days + 1)
        else:
            if days < 10:
                return Fu("中伏", days + 11)
            start_calendar = start_calendar + timedelta(days=10)
            days = ExactDate.getDaysBetweenDate(start_calendar, current_calendar)
            if days < 10:
                return Fu("末伏", days + 1)
        return None

    def getLiuYao(self):
        """
        获取六曜
        :return: 六曜
        """
        return LunarUtil.LIU_YAO[(abs(self.__month) + self.__day - 2) % 6]

    def getWuHou(self):
        """
        获取物候
        :return: 物候
        """
        jie_qi = self.getPrevJieQi(True)
        name = jie_qi.getName()
        offset = 0
        for i in range(0, len(Lunar.JIE_QI)):
            if name == Lunar.JIE_QI[i]:
                offset = i
                break
        start_solar = jie_qi.getSolar()
        days = ExactDate.getDaysBetween(start_solar.getYear(), start_solar.getMonth(), start_solar.getDay(), self.__solar.getYear(), self.__solar.getMonth(), self.__solar.getDay())
        index = int(days / 5)
        if index > 2:
            index = 2
        return LunarUtil.WU_HOU[(offset * 3 + index) % len(LunarUtil.WU_HOU)]

    def getHou(self):
        jie_qi = self.getPrevJieQi(True)
        start_solar = jie_qi.getSolar()
        days = ExactDate.getDaysBetween(start_solar.getYear(), start_solar.getMonth(), start_solar.getDay(), self.__solar.getYear(), self.__solar.getMonth(), self.__solar.getDay())
        size = len(LunarUtil.HOU) - 1
        offset = int(days / 5)
        if offset > size:
            offset = size
        return "%s %s" % (jie_qi.getName(), LunarUtil.HOU[offset])

    def getDayLu(self):
        """
        获取日禄
        :return: 日禄
        """
        gan = LunarUtil.LU[self.getDayGan()]
        zhi = None
        if self.getDayZhi() in LunarUtil.LU:
            zhi = LunarUtil.LU[self.getDayZhi()]
        lu = gan + "命互禄"
        if zhi is not None:
            lu += " " + zhi + "命进禄"
        return lu

    def getTime(self):
        """
        获取时辰
        :return: 时辰
        """
        return LunarTime.fromYmdHms(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)

    def getTimes(self):
        """
        获取当天的时辰列表
        :return: 时辰列表
        """
        times = [LunarTime.fromYmdHms(self.__year, self.__month, self.__day, 0, 0, 0)]
        for i in range(0, 12):
            times.append(LunarTime.fromYmdHms(self.__year, self.__month, self.__day, (i+1) * 2-1, 0, 0))
        return times

    def getFoto(self):
        """
        获取佛历
        :return: 佛历
        """
        from . import Foto
        return Foto.fromLunar(self)

    def getTao(self):
        """
        获取道历
        :return: 道历
        """
        from . import Tao
        return Tao.fromLunar(self)
