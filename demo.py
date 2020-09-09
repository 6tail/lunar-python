# -*- coding: utf-8 -*-
from lunar_python import Lunar, Solar
from lunar_python.util import HolidayUtil

# 节气表
lunar = Solar.fromYmd(2022, 7, 15).getLunar()
jieQi = lunar.getJieQiTable()
for k in lunar.getJieQiList():
    print k + ' = ' + jieQi[k].toYmdHms()
print ''

# 八字
baZi = lunar.getEightChar()
print baZi.getYear() + ' ' + baZi.getMonth() + ' ' + baZi.getDay() + ' ' + baZi.getTime()

# 八字五行
print baZi.getYearWuXing() + ' ' + baZi.getMonthWuXing() + ' ' + baZi.getDayWuXing() + ' ' + baZi.getTimeWuXing()

# 八字天干十神
print baZi.getYearShiShenGan() + ' ' + baZi.getMonthShiShenGan() + ' ' + baZi.getDayShiShenGan() + ' ' + baZi.getTimeShiShenGan()

# 八字地支十神
print baZi.getYearShiShenZhi()[0] + ' ' + baZi.getMonthShiShenZhi()[0] + ' ' + baZi.getDayShiShenZhi()[0] + ' ' + baZi.getTimeShiShenZhi()[0]

# 遍历八字年支十神
for v in baZi.getYearShiShenZhi():
    print v
print ''

# 遍历八字月支十神
for v in baZi.getMonthShiShenZhi():
    print v
print ''

# 遍历八字日支十神
for v in baZi.getDayShiShenZhi():
    print v
print ''

# 遍历八字时支十神
for v in baZi.getTimeShiShenZhi():
    print v
print ''

solar = Solar(1983, 2, 15, 20, 0, 0)
lunar = solar.getLunar()
baZi = lunar.getEightChar()

# 女运
yun = baZi.getYun(0)
print '阳历' + solar.toYmdHms() + '出生'
print '出生' + str(yun.getStartYear()) + '年' + str(yun.getStartMonth()) + '个月' + str(yun.getStartDay()) + '天后起运'
print '阳历' + yun.getStartSolar().toYmd() + '后起运'
print ''

# 大运
daYunArr = yun.getDaYun()
for i in range(0, len(daYunArr)):
    daYun = daYunArr[i]
    print '大运[' + str(i) + '] ' + str(daYun.getStartYear()) + '年 ' + str(daYun.getStartAge()) + '岁 ' + daYun.getGanZhi()
print ''

# 大运[0] 流年
liuNianArr = daYunArr[0].getLiuNian()
for i in range(0, len(liuNianArr)):
    liuNian = liuNianArr[i]
    print '流年[' + str(i) + '] ' + str(liuNian.getYear()) + '年 ' + str(liuNian.getAge()) + '岁 ' + liuNian.getGanZhi()
print ''

# 大运[0] 小运
xiaoYunArr = daYunArr[0].getXiaoYun()
for i in range(0, len(xiaoYunArr)):
    xiaoYun = xiaoYunArr[i]
    print '小运[' + str(i) + '] ' + str(xiaoYun.getYear()) + '年 ' + str(xiaoYun.getAge()) + '岁 ' + xiaoYun.getGanZhi()
print ''

# 流年[0] 流月
liuYueArr = liuNianArr[0].getLiuYue()
for i in range(0, len(liuYueArr)):
    liuYue = liuYueArr[i]
    print '流月[' + str(i) + '] ' + str(liuYue.getMonthInChinese()) + '月 ' + liuYue.getGanZhi()
print ''

# 通过指定年月日初始化阴历
lunar = Lunar.fromYmd(1986, 4, 21)

# 打印阴历
print lunar.toFullString()

# 阴历转阳历并打印
print lunar.getSolar().toFullString()

# 节假日信息
print HolidayUtil.getHoliday('2020-05-02')

# 儒略日
solar = Solar.fromYmd(2020, 7, 15)
print solar.getJulianDay()

solar = Solar.fromJulianDay(2459045.5)
print solar.toYmdHms()
print ''

# 八字转阳历
l = Solar.fromBaZi("庚子", "戊子", "己卯", "庚午")
for d in l:
    print d.toFullString()
