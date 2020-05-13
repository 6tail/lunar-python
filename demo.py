# -*- coding: utf-8 -*-
from lunar_python import Lunar
from lunar_python.util import HolidayUtil

# 通过指定年月日初始化阴历
lunar = Lunar.fromYmd(1986, 4, 21)

# 打印阴历
print lunar.toFullString()

# 阴历转阳历并打印
print lunar.getSolar().toFullString()

# 节假日信息
print HolidayUtil.getHoliday('2020-05-02')
