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

solar = Solar(1988, 2, 15, 23, 30, 0)
lunar = solar.getLunar()
baZi = lunar.getEightChar()
print baZi.getYear() + ' ' + baZi.getMonth() + ' ' + baZi.getDay() + ' ' + baZi.getTime()

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

date = Solar.fromYmd(2020, 1, 23)
print("2020-01-24" == date.next(1).toString())
# 仅工作日，跨越春节假期
print("2020-02-03" == date.nextWorkday(1).toString())

date = Solar.fromYmd(2020, 2, 3)
print("2020-01-31" == date.next(-3).toString())
# 仅工作日，跨越春节假期
print("2020-01-21" == date.nextWorkday(-3).toString())

date = Solar.fromYmd(2020, 2, 9)
print("2020-02-15" == date.next(6).toString())
# 仅工作日，跨越周末
print("2020-02-17" == date.nextWorkday(6).toString())

date = Solar.fromYmd(2020, 1, 17)
print("2020-01-18" == date.next(1).toString())
# 仅工作日，周日调休按上班算
print("2020-01-19" == date.nextWorkday(1).toString())

print("2020-01-01 元旦节 2020-01-01" == HolidayUtil.getHoliday("2020-01-01").toString())

# 将2020-01-01修改为春节
HolidayUtil.fix(None, "202001011120200101")
print("2020-01-01 春节 2020-01-01" == HolidayUtil.getHoliday("2020-01-01").toString())

# 追加2099-01-01为元旦节
HolidayUtil.fix(None, "209901010120990101")
print("2099-01-01 元旦节 2099-01-01" == HolidayUtil.getHoliday("2099-01-01").toString())

# 将2020-01-01修改为春节，并追加2099-01-01为元旦节
HolidayUtil.fix(None, "202001011120200101209901010120990101")
print("2020-01-01 春节 2020-01-01" == HolidayUtil.getHoliday("2020-01-01").toString())
print("2099-01-01 元旦节 2099-01-01" == HolidayUtil.getHoliday("2099-01-01").toString())

# 更改节假日名称
names = []
for i in range(0, len(HolidayUtil.NAMES)):
    names.append(HolidayUtil.NAMES[i])
names[0] = "元旦"
names[1] = "大年初一"

HolidayUtil.fix(names, None)
print("2020-01-01 大年初一 2020-01-01" == HolidayUtil.getHoliday("2020-01-01").toString())
print("2099-01-01 元旦 2099-01-01" == HolidayUtil.getHoliday("2099-01-01").toString())

# 追加节假日名称和数据
names = []
for i in range(0, len(HolidayUtil.NAMES)):
    names.append(HolidayUtil.NAMES[i])
names.append("我的生日")
names.append("结婚纪念日")
names.append("她的生日")

HolidayUtil.fix(names, "20210529912021052920211111:12021111120211201;120211201")
print("2021-05-29 我的生日 2021-05-29" == HolidayUtil.getHoliday("2021-05-29").toString())
print("2021-11-11 结婚纪念日 2021-11-11" == HolidayUtil.getHoliday("2021-11-11").toString())
print("2021-12-01 她的生日 2021-12-01" == HolidayUtil.getHoliday("2021-12-01").toString())

# 节日
solar = Solar.fromYmd(2020, 11, 26)
festivals = solar.getFestivals()
for i in range(0, len(festivals)):
    print(festivals[i])

solar = Solar.fromYmd(2020, 6, 21)
festivals = solar.getFestivals()
for i in range(0, len(festivals)):
    print(festivals[i])

solar = Solar.fromYmd(2021, 5, 9)
festivals = solar.getFestivals()
for i in range(0, len(festivals)):
    print(festivals[i])

solar = Solar.fromYmd(1986, 11, 27)
festivals = solar.getFestivals()
for i in range(0, len(festivals)):
    print(festivals[i])

solar = Solar.fromYmd(1985, 6, 16)
festivals = solar.getFestivals()
for i in range(0, len(festivals)):
    print(festivals[i])

solar = Solar.fromYmd(1984, 5, 13)
festivals = solar.getFestivals()
for i in range(0, len(festivals)):
    print(festivals[i])

# 旬
solar = Solar.fromYmdHms(2020, 11, 19, 0, 0, 0)
lunar = solar.getLunar()
# 甲午
print(lunar.getYearXun())

# 旬空(空亡)
# 辰巳
print(lunar.getYearXunKong())
# 午未
print(lunar.getMonthXunKong())
# 戌亥
print(lunar.getDayXunKong())

# 八字日柱旬空(空亡)
solar = Solar.fromYmdHms(1990, 12, 23, 8, 37, 0)
lunar = solar.getLunar()
eightChar = lunar.getEightChar()
# 子丑
print(eightChar.getDayXunKong())
