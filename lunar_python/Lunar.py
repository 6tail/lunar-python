# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from math import pi, cos, sin
from .util import LunarUtil, SolarUtil


class Lunar:
    """
    阴历日期
    """

    __RAD_PER_DEGREE = pi / 180
    __DEGREE_PER_RAD = 180 / pi
    __SECOND_PER_RAD = 180 * 3600 / pi
    __JIE_QI = ("冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪")
    __E10 = (
        1.75347045673, 0.00000000000, 0.0000000000, 0.03341656456, 4.66925680417, 6283.0758499914, 0.00034894275, 4.62610241759, 12566.1516999828, 0.00003417571, 2.82886579606, 3.5231183490, 0.00003497056, 2.74411800971, 5753.3848848968, 0.00003135896, 3.62767041758, 77713.7714681205, 0.00002676218, 4.41808351397, 7860.4193924392, 0.00002342687, 6.13516237631, 3930.2096962196, 0.00001273166, 2.03709655772, 529.6909650946, 0.00001324292, 0.74246356352, 11506.7697697936, 0.00000901855, 2.04505443513, 26.2983197998, 0.00001199167, 1.10962944315, 1577.3435424478, 0.00000857223, 3.50849156957, 398.1490034082, 0.00000779786, 1.17882652114, 5223.6939198022, 0.00000990250, 5.23268129594, 5884.9268465832, 0.00000753141, 2.53339053818, 5507.5532386674, 0.00000505264, 4.58292563052,
        18849.2275499742, 0.00000492379, 4.20506639861, 775.5226113240, 0.00000356655, 2.91954116867, 0.0673103028, 0.00000284125, 1.89869034186, 796.2980068164, 0.00000242810, 0.34481140906, 5486.7778431750, 0.00000317087, 5.84901952218, 11790.6290886588, 0.00000271039, 0.31488607649, 10977.0788046990, 0.00000206160, 4.80646606059, 2544.3144198834, 0.00000205385, 1.86947813692, 5573.1428014331, 0.00000202261, 2.45767795458, 6069.7767545534, 0.00000126184, 1.08302630210, 20.7753954924, 0.00000155516, 0.83306073807, 213.2990954380, 0.00000115132, 0.64544911683, 0.9803210682, 0.00000102851, 0.63599846727, 4694.0029547076, 0.00000101724, 4.26679821365, 7.1135470008, 0.00000099206, 6.20992940258, 2146.1654164752, 0.00000132212, 3.41118275555, 2942.4634232916, 0.00000097607, 0.68101272270,
        155.4203994342, 0.00000085128, 1.29870743025, 6275.9623029906, 0.00000074651, 1.75508916159, 5088.6288397668, 0.00000101895, 0.97569221824, 15720.8387848784, 0.00000084711, 3.67080093025, 71430.6956181291, 0.00000073547, 4.67926565481, 801.8209311238, 0.00000073874, 3.50319443167, 3154.6870848956, 0.00000078756, 3.03698313141, 12036.4607348882, 0.00000079637, 1.80791330700, 17260.1546546904, 0.00000085803, 5.98322631256, 161000.6857376741, 0.00000056963, 2.78430398043, 6286.5989683404, 0.00000061148, 1.81839811024, 7084.8967811152, 0.00000069627, 0.83297596966, 9437.7629348870, 0.00000056116, 4.38694880779, 14143.4952424306, 0.00000062449, 3.97763880587, 8827.3902698748, 0.00000051145, 0.28306864501, 5856.4776591154, 0.00000055577, 3.47006009062, 6279.5527316424, 0.00000041036,
        5.36817351402, 8429.2412664666, 0.00000051605, 1.33282746983, 1748.0164130670, 0.00000051992, 0.18914945834, 12139.5535091068, 0.00000049000, 0.48735065033, 1194.4470102246, 0.00000039200, 6.16832995016, 10447.3878396044, 0.00000035566, 1.77597314691, 6812.7668150860, 0.00000036770, 6.04133859347, 10213.2855462110, 0.00000036596, 2.56955238628, 1059.3819301892, 0.00000033291, 0.59309499459, 17789.8456197850, 0.00000035954, 1.70876111898, 2352.8661537718
    )

    __E11 = (
        6283.31966747491, 0.00000000000, 0.0000000000, 0.00206058863, 2.67823455584, 6283.0758499914, 0.00004303430, 2.63512650414, 12566.1516999828, 0.00000425264, 1.59046980729, 3.5231183490, 0.00000108977, 2.96618001993, 1577.3435424478, 0.00000093478, 2.59212835365, 18849.2275499742, 0.00000119261, 5.79557487799, 26.2983197998, 0.00000072122, 1.13846158196, 529.6909650946, 0.00000067768, 1.87472304791, 398.1490034082, 0.00000067327, 4.40918235168, 5507.5532386674, 0.00000059027, 2.88797038460, 5223.6939198022, 0.00000055976, 2.17471680261, 155.4203994342, 0.00000045407, 0.39803079805, 796.2980068164, 0.00000036369, 0.46624739835, 775.5226113240, 0.00000028958, 2.64707383882, 7.1135470008, 0.00000019097, 1.84628332577, 5486.7778431750, 0.00000020844, 5.34138275149, 0.9803210682,
        0.00000018508, 4.96855124577, 213.2990954380, 0.00000016233, 0.03216483047, 2544.3144198834, 0.00000017293, 2.99116864949, 6275.9623029906
    )

    __E12 = (0.00052918870, 0.00000000000, 0.0000000000, 0.00008719837, 1.07209665242, 6283.0758499914, 0.00000309125, 0.86728818832, 12566.1516999828, 0.00000027339, 0.05297871691, 3.5231183490, 0.00000016334, 5.18826691036, 26.2983197998, 0.00000015752, 3.68457889430, 155.4203994342, 0.00000009541, 0.75742297675, 18849.2275499742, 0.00000008937, 2.05705419118, 77713.7714681205, 0.00000006952, 0.82673305410, 775.5226113240, 0.00000005064, 4.66284525271, 1577.3435424478)
    __E13 = (0.00000289226, 5.84384198723, 6283.0758499914, 0.00000034955, 0.00000000000, 0.0000000000, 0.00000016819, 5.48766912348, 12566.1516999828)
    __E14 = (0.00000114084, 3.14159265359, 0.0000000000, 0.00000007717, 4.13446589358, 6283.0758499914, 0.00000000765, 3.83803776214, 12566.1516999828)
    __E15 = (0.00000000878, 3.14159265359, 0.0000000000)
    __E20 = (0.00000279620, 3.19870156017, 84334.6615813083, 0.00000101643, 5.42248619256, 5507.5532386674, 0.00000080445, 3.88013204458, 5223.6939198022, 0.00000043806, 3.70444689758, 2352.8661537718, 0.00000031933, 4.00026369781, 1577.3435424478, 0.00000022724, 3.98473831560, 1047.7473117547, 0.00000016392, 3.56456119782, 5856.4776591154, 0.00000018141, 4.98367470263, 6283.0758499914, 0.00000014443, 3.70275614914, 9437.7629348870, 0.00000014304, 3.41117857525, 10213.2855462110)
    __E21 = (0.00000009030, 3.89729061890, 5507.5532386674, 0.00000006177, 1.73038850355, 5223.6939198022)
    __GXC_E = (0.016708634, -0.000042037, -0.0000001267)
    __GXC_P = (102.93735 / __DEGREE_PER_RAD, 1.71946 / __DEGREE_PER_RAD, 0.00046 / __DEGREE_PER_RAD)
    __GXC_L = (280.4664567 / __DEGREE_PER_RAD, 36000.76982779 / __DEGREE_PER_RAD, 0.0003032028 / __DEGREE_PER_RAD, 1 / 49931000 / __DEGREE_PER_RAD, -1 / 153000000 / __DEGREE_PER_RAD)
    __GXC_K = 20.49552 / __SECOND_PER_RAD
    __ZD = (
        2.1824391966, -33.757045954, 0.0000362262, 3.7340E-08, -2.8793E-10, -171996, -1742, 92025, 89, 3.5069406862, 1256.663930738, 0.0000105845, 6.9813E-10, -2.2815E-10, -13187, -16, 5736, -31, 1.3375032491, 16799.418221925, -0.0000511866, 6.4626E-08, -5.3543E-10, -2274, -2, 977, -5, 4.3648783932, -67.514091907, 0.0000724525, 7.4681E-08, -5.7586E-10, 2062, 2, -895, 5, 0.0431251803, -628.301955171, 0.0000026820, 6.5935E-10, 5.5705E-11, -1426, 34, 54, -1, 2.3555557435, 8328.691425719, 0.0001545547, 2.5033E-07, -1.1863E-09, 712, 1, -7, 0, 3.4638155059, 1884.965885909, 0.0000079025, 3.8785E-11, -2.8386E-10, -517, 12, 224, -6, 5.4382493597, 16833.175267879, -0.0000874129, 2.7285E-08, -2.4750E-10, -386, -4, 200, 0, 3.6930589926, 25128.109647645, 0.0001033681, 3.1496E-07, -1.7218E-09, -301,
        0, 129, -1, 3.5500658664, 628.361975567, 0.0000132664, 1.3575E-09, -1.7245E-10, 217, -5, -95, 3
    )

    def __init__(self, lunarYear, lunarMonth, lunarDay, hour, minute, second):
        self.__year = lunarYear
        self.__month = lunarMonth
        self.__day = lunarDay
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__dayOffset = LunarUtil.computeAddDays(lunarYear, lunarMonth, lunarDay)
        self.__solar = self.__toSolar()
        self.__jieQi = {}
        self.__compute()

    def __toSolar(self):
        from .Solar import Solar
        c = datetime(SolarUtil.BASE_YEAR, SolarUtil.BASE_MONTH, SolarUtil.BASE_DAY, self.__hour, self.__minute, self.__second)
        c = c + timedelta(days=self.__dayOffset)
        return Solar.fromDate(c)

    def __compute(self):
        self.__computeJieQi()
        self.__computeYear()
        self.__computeMonth()
        self.__computeDay()
        self.__computeTime()
        self.__computeWeek()

    def __mrad(self, rad):
        pi2 = 2 * pi
        rad = rad % pi2
        return rad + pi2 if rad < 0 else rad

    def __gxc(self, t, pos):
        t1 = t / 36525
        t2 = t1 * t1
        t3 = t2 * t1
        t4 = t3 * t1
        l = Lunar.__GXC_L[0] + Lunar.__GXC_L[1] * t1 + Lunar.__GXC_L[2] * t2 + Lunar.__GXC_L[3] * t3 + Lunar.__GXC_L[4] * t4
        p = Lunar.__GXC_P[0] + Lunar.__GXC_P[1] * t1 + Lunar.__GXC_P[2] * t2
        e = Lunar.__GXC_E[0] + Lunar.__GXC_E[1] * t1 + Lunar.__GXC_E[2] * t2
        dl = l - pos[0]
        dp = p - pos[0]
        pos[0] -= Lunar.__GXC_K * (cos(dl) - e * cos(dp)) / cos(pos[1])
        pos[1] -= Lunar.__GXC_K * sin(pos[1]) * (sin(dl) - e * sin(dp))
        pos[0] = self.__mrad(pos[0])

    def __enn(self, f, ennt):
        v = 0
        for i in range(0, len(f), 3):
            v += f[i] * cos(f[i + 1] + ennt * f[i + 2])
        return v

    def __calEarth(self, t):
        t1 = t / 365250
        r = []
        t2 = t1 * t1
        t3 = t2 * t1
        t4 = t3 * t1
        t5 = t4 * t1
        r.append(self.__mrad(self.__enn(Lunar.__E10, t1) + self.__enn(Lunar.__E11, t1) * t1 + self.__enn(Lunar.__E12, t1) * t2 + self.__enn(Lunar.__E13, t1) * t3 + self.__enn(Lunar.__E14, t1) * t4 + self.__enn(Lunar.__E15, t1) * t5))
        r.append(self.__enn(Lunar.__E20, t1) + self.__enn(Lunar.__E21, t1) * t1)
        return r

    def __hjzd(self, t):
        lon = 0
        t1 = t / 36525
        t2 = t1 * t1
        t3 = t2 * t1
        t4 = t3 * t1
        for i in range(0, len(Lunar.__ZD), 9):
            c = Lunar.__ZD[i] + Lunar.__ZD[i + 1] * t1 + Lunar.__ZD[i + 2] * t2 + Lunar.__ZD[i + 3] * t3 + Lunar.__ZD[i + 4] * t4
            lon += (Lunar.__ZD[i + 5] + Lunar.__ZD[i + 6] * t1 / 10) * sin(c)
        lon /= Lunar.__SECOND_PER_RAD * 10000
        return lon

    def __calRad(self, t, rad):
        pos = self.__calEarth(t)
        pos[0] += pi
        pos[1] = -pos[1]
        self.__gxc(t, pos)
        pos[0] += self.__hjzd(t)
        return self.__mrad(rad - pos[0])

    def __calJieQi(self, t1, degree):
        t2 = t1
        t = 0
        t2 += 360
        rad = degree * Lunar.__RAD_PER_DEGREE
        v1 = self.__calRad(t1, rad)
        v2 = self.__calRad(t2, rad)
        if v1 < v2:
            v2 -= 2 * pi

        k = 1
        for i in range(0, 10):
            k2 = (v2 - v1) / (t2 - t1)
            if abs(k2) > 1e-15:
                k = k2
            t = t1 - v1 / k
            v = self.__calRad(t, rad)
            if v > 1:
                v -= 2 * pi
            if abs(v) < 1e-8:
                break
            t1 = t2
            v1 = v2
            t2 = t
            v2 = v
        return t

    def __computeJieQi(self):
        from .Solar import Solar
        jd = 365.2422 * (self.__solar.getYear() - 2001)
        for i in range(0, len(Lunar.__JIE_QI)):
            t = self.__calJieQi(jd + i * 15.2, i * 15 - 90) + Solar.J2000 + 8.0 / 24
            self.__jieQi[Lunar.__JIE_QI[i]] = Solar.fromJulianDay(t)

    def __computeYear(self):
        yearGanIndex = (self.__year + LunarUtil.BASE_YEAR_GAN_ZHI_INDEX) % 10
        yearZhiIndex = (self.__year + LunarUtil.BASE_YEAR_GAN_ZHI_INDEX) % 12

        # 以立春作为新一年的开始的干支纪年
        g = yearGanIndex
        z = yearZhiIndex

        # 精确的干支纪年，以立春交接时刻为准
        gExact = yearGanIndex
        zExact = yearZhiIndex

        if self.__year == self.__solar.getYear():
            # 获取立春的阳历时刻
            liChun = self.__jieQi["立春"]
            # 立春日期判断
            if self.__solar.toYmd() < liChun.toYmd():
                g -= 1
                if g < 0:
                    g += 10
                z -= 1
                if z < 0:
                    z += 12
            # 立春交接时刻判断
            if self.__solar.toYmdHms() < liChun.toYmdHms():
                gExact -= 1
                if gExact < 0:
                    gExact += 10
                zExact -= 1
                if zExact < 0:
                    zExact += 12

        self.__yearGanIndex = yearGanIndex
        self.__yearZhiIndex = yearZhiIndex

        self.__yearGanIndexByLiChun = g
        self.__yearZhiIndexByLiChun = z

        self.__yearGanIndexExact = gExact
        self.__yearZhiIndexExact = zExact

    def __computeMonth(self):
        # 干偏移值（以立春当天起算）
        gOffset = ((self.__yearGanIndexByLiChun % 5 + 1) * 2) % 10
        # 干偏移值（以立春交接时刻起算）
        gOffsetExact = ((self.__yearGanIndexExact % 5 + 1) * 2) % 10

        # 序号：大雪到小寒之间 - 2，小寒到立春之间 - 1，立春之后0
        index = -2
        start = None
        for jie in LunarUtil.JIE:
            end = self.__jieQi[jie]
            ymd = self.__solar.toYmd()
            symd = ymd if start is None else start.toYmd()
            eymd = end.toYmd()
            if symd <= ymd < eymd:
                break
            start = end
            index += 1
        if index < 0:
            index += 12

        monthGanIndex = (index + gOffset) % 10
        monthZhiIndex = (index + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12

        # 序号：大雪到小寒之间-2，小寒到立春之间-1，立春之后0
        indexExact = -2
        start = None
        for jie in LunarUtil.JIE:
            end = self.__jieQi[jie]
            time = self.__solar.toYmdHms()
            stime = time if start is None else start.toYmdHms()
            etime = end.toYmdHms()
            if stime <= time < etime:
                break
            start = end
            indexExact += 1
        if indexExact < 0:
            indexExact += 12

        self.__monthGanIndex = monthGanIndex
        self.__monthZhiIndex = monthZhiIndex
        self.__monthGanIndexExact = (indexExact + gOffsetExact) % 10
        self.__monthZhiIndexExact = (indexExact + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12

    def __computeDay(self):
        addDays = (self.__dayOffset + LunarUtil.BASE_DAY_GAN_ZHI_INDEX) % 60
        dayGanIndex = addDays % 10
        dayZhiIndex = addDays % 12

        self.__dayGanIndex = dayGanIndex
        self.__dayZhiIndex = dayZhiIndex

        dayGanExact = dayGanIndex
        dayZhiExact = dayZhiIndex

        hm = ("0" if self.__hour < 10 else "") + str(self.__hour) + ":" + ("0" if self.__minute < 10 else "") + str(self.__minute)
        if "23:00" <= hm <= "23:59":
            dayGanExact += 1
            if dayGanExact >= 10:
                dayGanExact -= 10
            dayZhiExact += 1
            if dayZhiExact >= 12:
                dayZhiExact -= 12
        self.__dayGanIndexExact = dayGanExact
        self.__dayZhiIndexExact = dayZhiExact

    def __computeTime(self):
        timeZhiIndex = LunarUtil.getTimeZhiIndex(("0" if self.__hour < 10 else "") + str(self.__hour) + ":" + ("0" if self.__minute < 10 else "") + str(self.__minute))
        self.__timeZhiIndex = timeZhiIndex
        self.__timeGanIndex = (self.__dayGanIndexExact % 5 * 2 + timeZhiIndex) % 10

    def __computeWeek(self):
        self.__weekIndex = (self.__dayOffset + LunarUtil.BASE_WEEK_INDEX) % 7

    @staticmethod
    def fromYmdHms(lunarYear, lunarMonth, lunarDay, hour, minute, second):
        return Lunar(lunarYear, lunarMonth, lunarDay, hour, minute, second)

    @staticmethod
    def fromYmd(lunarYear, lunarMonth, lunarDay):
        return Lunar(lunarYear, lunarMonth, lunarDay, 0, 0, 0)

    @staticmethod
    def fromDate(date):
        from .Solar import Solar
        solar = Solar.fromDate(date)
        y = solar.getYear()
        m = solar.getMonth()
        d = solar.getDay()
        if y < 2000:
            startYear = SolarUtil.BASE_YEAR
            startMonth = SolarUtil.BASE_MONTH
            startDay = SolarUtil.BASE_DAY
            lunarYear = LunarUtil.BASE_YEAR
            lunarMonth = LunarUtil.BASE_MONTH
            lunarDay = LunarUtil.BASE_DAY
        else:
            startYear = SolarUtil.BASE_YEAR + 99
            startMonth = 1
            startDay = 1
            lunarYear = LunarUtil.BASE_YEAR + 99
            lunarMonth = 11
            lunarDay = 25
        diff = 0
        for i in range(startYear, y):
            diff += 365
            if SolarUtil.isLeapYear(i):
                diff += 1
        for i in range(startMonth, m):
            diff += SolarUtil.getDaysOfMonth(y, i)
        diff += d - startDay
        lunarDay += diff
        lastDate = LunarUtil.getDaysOfMonth(lunarYear, lunarMonth)
        while lunarDay > lastDate:
            lunarDay -= lastDate
            lunarMonth = LunarUtil.nextMonth(lunarYear, lunarMonth)
            if lunarMonth == 1:
                lunarYear += 1
            lastDate = LunarUtil.getDaysOfMonth(lunarYear, lunarMonth)
        year = lunarYear
        month = lunarMonth
        day = lunarDay
        hour = solar.getHour()
        minute = solar.getMinute()
        second = solar.getSecond()
        return Lunar(year, month, day, hour, minute, second)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

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

    def getDayZhi(self):
        return LunarUtil.ZHI[self.__dayZhiIndex + 1]

    def getDayZhiExact(self):
        return LunarUtil.ZHI[self.__dayZhiIndexExact + 1]

    def getDayInGanZhi(self):
        return self.getDayGan() + self.getDayZhi()

    def getDayInGanZhiExact(self):
        return self.getDayGanExact() + self.getDayZhiExact()

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
        return LunarUtil.POSITION_XI[self.__dayGanIndex + 1]

    def getPositionXiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionXi()]

    def getPositionYangGui(self):
        return LunarUtil.POSITION_YANG_GUI[self.__dayGanIndex + 1]

    def getPositionYangGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYangGui()]

    def getPositionYinGui(self):
        return LunarUtil.POSITION_YIN_GUI[self.__dayGanIndex + 1]

    def getPositionYinGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYinGui()]

    def getPositionFu(self):
        return LunarUtil.POSITION_FU[self.__dayGanIndex + 1]

    def getPositionFuDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionFu()]

    def getPositionCai(self):
        return LunarUtil.POSITION_CAI[self.__dayGanIndex + 1]

    def getPositionCaiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionCai()]

    def getChong(self):
        return self.getDayChong()

    def getDayChong(self):
        return LunarUtil.CHONG[self.__dayZhiIndex + 1]

    def getTimeChong(self):
        return LunarUtil.CHONG[self.__timeZhiIndex + 1]

    def getChongGan(self):
        return self.getDayChongGan()

    def getDayChongGan(self):
        return LunarUtil.CHONG_GAN[self.__dayGanIndex + 1]

    def getTimeChongGan(self):
        return LunarUtil.CHONG_GAN[self.__timeGanIndex + 1]

    def getChongGanTie(self):
        return self.getDayChongGanTie()

    def getDayChongGanTie(self):
        return LunarUtil.CHONG_GAN_TIE[self.getDayGan()]

    def getTimeChongGanTie(self):
        return LunarUtil.CHONG_GAN_TIE[self.getTimeGan()]

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
        return '(' + self.getDayChongGan() + self.getDayChong() + ')' + self.getDayChongShengXiao()

    def getTimeChongDesc(self):
        return '(' + self.getTimeChongGan() + self.getTimeChong() + ')' + self.getTimeChongShengXiao()

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

    def getJie(self):
        for i in range(0, len(LunarUtil.JIE)):
            jie = LunarUtil.JIE[i]
            d = self.__jieQi[jie]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return jie
        return ""

    def getQi(self):
        for i in range(0, len(LunarUtil.QI)):
            qi = LunarUtil.QI[i]
            d = self.__jieQi[qi]
            if d.getYear() == self.__solar.getYear() and d.getMonth() == self.__solar.getMonth() and d.getDay() == self.__solar.getDay():
                return qi
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
        l = []
        md = str(self.__month) + "-" + str(self.__day)
        if md in LunarUtil.FESTIVAL:
            l.append(LunarUtil.FESTIVAL[md])
        return l

    def getOtherFestivals(self):
        l = []
        md = str(self.__month) + "-" + str(self.__day)
        if md in LunarUtil.OTHER_FESTIVAL:
            fs = LunarUtil.OTHER_FESTIVAL[md]
            for f in fs:
                l.append(f)
        return l

    def getBaZi(self):
        l = []
        l.append(self.getYearInGanZhiExact())
        l.append(self.getMonthInGanZhiExact())
        l.append(self.getDayInGanZhiExact())
        l.append(self.getTimeInGanZhi())
        return l

    def getBaZiWuXing(self):
        baZi = self.getBaZi()
        l = []
        for i in range(0, len(baZi)):
            ganZhi = baZi[i]
            gan = ganZhi[0:1]
            zhi = ganZhi[1:]
            l.append(LunarUtil.WU_XING_GAN[gan] + LunarUtil.WU_XING_ZHI[zhi])
        return l

    def getBaZiNaYin(self):
        baZi = self.getBaZi()
        l = []
        for i in range(0, len(baZi)):
            ganZhi = baZi[i]
            l.append(LunarUtil.NAYIN[ganZhi])
        return l

    def getBaZiShiShenGan(self):
        baZi = self.getBaZi()
        yearGan = baZi[0][0:1]
        monthGan = baZi[1][0:1]
        dayGan = baZi[2][0:1]
        timeGan = baZi[3][0:1]
        l = []
        l.append(LunarUtil.SHI_SHEN_GAN[dayGan + yearGan])
        l.append(LunarUtil.SHI_SHEN_GAN[dayGan + monthGan])
        l.append('日主')
        l.append(LunarUtil.SHI_SHEN_GAN[dayGan + timeGan])
        return l

    def getBaZiShiShenZhi(self):
        baZi = self.getBaZi()
        dayGan = baZi[2][0:1]
        l = []
        for i in range(0, len(baZi)):
            ganZhi = baZi[i]
            zhi = ganZhi[1:]
            l.append(LunarUtil.SHI_SHEN_ZHI[dayGan + zhi + LunarUtil.ZHI_HIDE_GAN[zhi][0]])
        return l

    def getZhiXing(self):
        offset = self.__dayZhiIndex - self.__monthZhiIndex
        if offset < 0:
            offset += 12
        return LunarUtil.ZHI_XING[offset + 1]

    def getDayTianShen(self):
        monthZhi = self.getMonthZhi()
        offset = LunarUtil.ZHI_TIAN_SHEN_OFFSET[monthZhi]
        return LunarUtil.TIAN_SHEN[(self.__dayZhiIndex + offset) % 12 + 1]

    def getTimeTianShen(self):
        dayZhi = self.getDayZhiExact()
        offset = LunarUtil.ZHI_TIAN_SHEN_OFFSET[dayZhi]
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
        offset = self.__dayGanIndex - self.__dayZhiIndex
        if offset < 0:
            offset += 12
        return LunarUtil.POSITION_TAI_DAY[offset * 5 + self.__dayGanIndex]

    def getMonthPositionTai(self):
        m = self.__month
        if m < 0:
            return ""
        return LunarUtil.POSITION_TAI_MONTH[m - 1]

    def getDayYi(self):
        """
        获取每日宜
        :return: 宜
        """
        return LunarUtil.getDayYi(self.getMonthInGanZhiExact(), self.getDayInGanZhi())

    def getDayJi(self):
        """
        获取每日忌
        :return: 忌
        """
        return LunarUtil.getDayJi(self.getMonthInGanZhiExact(), self.getDayInGanZhi())

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

    def getJieQiTable(self):
        return self.__jieQi

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.getYearInChinese() + '年' + self.getMonthInChinese() + '月' + self.getDayInChinese()

    def toFullString(self):
        s = self.toString()
        s += ' ' + self.getYearInGanZhi() + '(' + self.getYearShengXiao() + ')年'
        s += ' ' + self.getMonthInGanZhi() + '(' + self.getMonthShengXiao() + ')月'
        s += ' ' + self.getDayInGanZhi() + '(' + self.getDayShengXiao() + ')日'
        s += ' ' + self.getTimeZhi() + '(' + self.getTimeShengXiao() + ')时'
        s += ' 纳音[' + self.getYearNaYin() + ' ' + self.getMonthNaYin() + ' ' + self.getDayNaYin() + ' ' + self.getTimeNaYin() + ']'
        s += ' 星期' + self.getWeekInChinese()
        for f in self.getFestivals():
            s += ' (' + f + ')'
        for f in self.getOtherFestivals():
            s += ' (' + f + ')'
        jq = self.getJie() + self.getQi()
        if len(jq) > 0:
            s += ' [' + jq + ']'
        s += ' ' + self.getGong() + '方' + self.getShou()
        s += ' 星宿[' + self.getXiu() + self.getZheng() + self.getAnimal() + '](' + self.getXiuLuck() + ')'
        s += ' 彭祖百忌[' + self.getPengZuGan() + ' ' + self.getPengZuZhi() + ']'
        s += ' 喜神方位[' + self.getPositionXi() + '](' + self.getPositionXiDesc() + ')'
        s += ' 阳贵神方位[' + self.getPositionYangGui() + '](' + self.getPositionYangGuiDesc() + ')'
        s += ' 阴贵神方位[' + self.getPositionYinGui() + '](' + self.getPositionYinGuiDesc() + ')'
        s += ' 福神方位[' + self.getPositionFu() + '](' + self.getPositionFuDesc() + ')'
        s += ' 财神方位[' + self.getPositionCai() + '](' + self.getPositionCaiDesc() + ')'
        s += ' 冲[' + self.getChongDesc() + ']'
        s += ' 煞[' + self.getSha() + ']'
        return s
