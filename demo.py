# -*- coding: utf-8 -*-
from lunar_python import Lunar, Solar
from lunar_python.util import HolidayUtil

# 节气表
lunar = Solar.fromYmd(2022, 7, 15).getLunar()
jieQi = lunar.getJieQiTable()
for k in lunar.getJieQiList():
    print k + ' = ' + jieQi[k].toYmdHms()
print ''

# 遍历八字
for v in lunar.getBaZi():
    print v
print ''

# 遍历八字五行
for v in lunar.getBaZiWuXing():
    print v
print ''

# 遍历八字天干十神
for v in lunar.getBaZiShiShenGan():
    print v
print ''

# 遍历八字地支十神
for v in lunar.getBaZiShiShenZhi():
    print v
print ''

# 遍历八字年支十神
for v in lunar.getBaZiShiShenYearZhi():
    print v
print ''

# 遍历八字月支十神
for v in lunar.getBaZiShiShenMonthZhi():
    print v
print ''

# 遍历八字日支十神
for v in lunar.getBaZiShiShenDayZhi():
    print v
print ''

# 遍历八字时支十神
for v in lunar.getBaZiShiShenTimeZhi():
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
