# -*- coding: utf-8 -*-
"""
lunar_python - 中国农历(阴历)、公历(阳历)、佛历、道历工具库

支持星座、儒略日、干支、生肖、节气、节日、彭祖百忌、吉神方位、
胎神方位、冲煞、纳音、星宿、八字、五行、十神、建除十二值星等。

时区支持：
- 默认时区为 Asia/Shanghai，包含1986-1991中国夏令时历史规则
- 支持传入任意 IANA 时区（如 "America/New_York"）或 tzinfo 对象
- 内部使用 UTC 进行天文计算，确保全球任意时区的准确性

示例：
    # 使用默认时区（Asia/Shanghai）
    solar = Solar.fromYmdHms(1991, 6, 1, 12, 0, 0)
    print(solar.isDST())  # True，1991年6月处于夏令时
    
    # 指定时区
    solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0, tz="America/New_York")
    solar_beijing = solar.toTimezone("Asia/Shanghai")  # 转换到北京时间
"""

# 异常类
from .exceptions import LunarException, DateException, SolarDateException, LunarDateException

# 核心类
from .JieQi import JieQi
from .NineStar import NineStar
from .EightChar import EightChar
from .ShuJiu import ShuJiu
from .Fu import Fu
from .Solar import Solar
from .SolarWeek import SolarWeek
from .SolarMonth import SolarMonth
from .SolarSeason import SolarSeason
from .SolarHalfYear import SolarHalfYear
from .SolarYear import SolarYear
from .LunarTime import LunarTime
from .Lunar import Lunar
from .LunarYear import LunarYear
from .LunarMonth import LunarMonth
from .Holiday import Holiday
from .FotoFestival import FotoFestival
from .Foto import Foto
from .TaoFestival import TaoFestival
from .Tao import Tao

# 公开 API
__all__ = [
    # 异常类
    'LunarException',
    'DateException',
    'SolarDateException',
    'LunarDateException',
    # 阳历相关
    'Solar',
    'SolarWeek',
    'SolarMonth',
    'SolarSeason',
    'SolarHalfYear',
    'SolarYear',
    # 阴历相关
    'Lunar',
    'LunarYear',
    'LunarMonth',
    'LunarTime',
    # 节气节日
    'JieQi',
    'Holiday',
    'ShuJiu',
    'Fu',
    # 八字命理
    'EightChar',
    'NineStar',
    # 佛历道历
    'Foto',
    'FotoFestival',
    'Tao',
    'TaoFestival',
]
