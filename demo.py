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
print baZi.getYear()+' '+baZi.getMonth()+' '+baZi.getDay()+' '+baZi.getTime()

# 八字五行
print baZi.getYearWuXing()+' '+baZi.getMonthWuXing()+' '+baZi.getDayWuXing()+' '+baZi.getTimeWuXing()

# 八字天干十神
print baZi.getYearShiShenGan()+' '+baZi.getMonthShiShenGan()+' '+baZi.getDayShiShenGan()+' '+baZi.getTimeShiShenGan()

# 八字地支十神
print baZi.getYearShiShenZhi()[0]+' '+baZi.getMonthShiShenZhi()[0]+' '+baZi.getDayShiShenZhi()[0]+' '+baZi.getTimeShiShenZhi()[0]

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
