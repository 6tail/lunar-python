# -*- coding: utf-8 -*-
"""
时区工具类 - 支持全球时区/夏令时历史规则和真太阳时

支持 IANA 时区名称（如 "Asia/Shanghai", "America/New_York"）和 tzinfo 对象。
默认时区为 Asia/Shanghai，包含中国1986-1991年夏令时历史规则。

真太阳时（True Solar Time）支持：
- 根据出生地经度计算真实的太阳时间
- 考虑时差方程（Equation of Time）修正
"""

import sys
import math
from datetime import datetime, timezone, timedelta

# 尝试导入 zoneinfo (Python 3.9+) 或 backports
try:
    from zoneinfo import ZoneInfo
except ImportError:
    try:
        from backports.zoneinfo import ZoneInfo
    except ImportError:
        ZoneInfo = None

# 如果 zoneinfo 不可用，尝试使用 pytz
try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    pytz = None
    HAS_PYTZ = False


class TimeZoneUtil:
    """
    时区工具类
    
    提供时区转换功能，支持：
    - IANA 时区字符串（推荐）：如 "Asia/Shanghai", "America/New_York"
    - tzinfo 对象：如 ZoneInfo("Asia/Shanghai"), pytz.timezone("Asia/Shanghai")
    - UTC 偏移量：如 timezone(timedelta(hours=8))
    
    默认时区为 Asia/Shanghai，包含中国1986-1991年夏令时历史规则。
    
    中国夏令时历史（1986-1991）：
    - 1986: 5月4日 02:00 -> 03:00, 9月14日 02:00 -> 01:00
    - 1987: 4月12日 02:00 -> 03:00, 9月13日 02:00 -> 01:00
    - 1988: 4月10日 02:00 -> 03:00, 9月11日 02:00 -> 01:00
    - 1989: 4月16日 02:00 -> 03:00, 9月17日 02:00 -> 01:00
    - 1990: 4月15日 02:00 -> 03:00, 9月16日 02:00 -> 01:00
    - 1991: 4月14日 02:00 -> 03:00, 9月15日 02:00 -> 01:00
    1991年后中国不再实行夏令时。
    """
    
    # 默认时区
    DEFAULT_TIMEZONE = "Asia/Shanghai"
    
    # UTC 时区
    UTC = timezone.utc
    
    # 北京时间固定偏移（不含DST，仅用于回退）
    BEIJING_OFFSET = timezone(timedelta(hours=8))
    
    @staticmethod
    def get_timezone(tz=None):
        """
        获取 tzinfo 对象
        
        :param tz: 时区，可以是：
            - None: 使用默认时区 (Asia/Shanghai)
            - str: IANA 时区名称，如 "Asia/Shanghai", "America/New_York"
            - tzinfo: 直接返回
        :return: tzinfo 对象
        :raises ValueError: 无效的时区名称
        """
        if tz is None:
            tz = TimeZoneUtil.DEFAULT_TIMEZONE
        
        if isinstance(tz, str):
            return TimeZoneUtil._get_timezone_by_name(tz)
        
        # 假设是 tzinfo 对象
        return tz
    
    @staticmethod
    def _get_timezone_by_name(name):
        """
        通过 IANA 名称获取时区
        
        :param name: IANA 时区名称
        :return: tzinfo 对象
        :raises ValueError: 无效的时区名称
        """
        if name == "UTC":
            return TimeZoneUtil.UTC
        
        # 优先使用 zoneinfo
        if ZoneInfo is not None:
            try:
                return ZoneInfo(name)
            except Exception:
                pass
        
        # 回退到 pytz
        if HAS_PYTZ:
            try:
                return pytz.timezone(name)
            except Exception:
                pass
        
        # 都不可用时的回退处理
        if name in ("Asia/Shanghai", "Asia/Chongqing", "Asia/Harbin", "PRC"):
            return TimeZoneUtil.BEIJING_OFFSET
        
        raise ValueError(f"无法识别的时区名称: {name}. 请安装 tzdata 或 pytz 包以支持完整时区功能。")
    
    @staticmethod
    def to_utc(dt, tz=None):
        """
        将本地时间转换为 UTC
        
        :param dt: datetime 对象（naive 或 aware）
        :param tz: 源时区（如果 dt 是 naive 的话使用此时区）
        :return: UTC 时间的 datetime 对象（aware）
        """
        if dt.tzinfo is not None:
            # 已经是 aware datetime，直接转换到 UTC
            return dt.astimezone(TimeZoneUtil.UTC)
        
        # naive datetime，使用指定时区或默认时区
        tzinfo = TimeZoneUtil.get_timezone(tz)
        
        # 对于 pytz 时区，需要使用 localize
        if HAS_PYTZ and hasattr(tzinfo, 'localize'):
            aware_dt = tzinfo.localize(dt)
        else:
            aware_dt = dt.replace(tzinfo=tzinfo)
        
        return aware_dt.astimezone(TimeZoneUtil.UTC)
    
    @staticmethod
    def from_utc(dt, tz=None):
        """
        将 UTC 时间转换为本地时间
        
        :param dt: UTC 时间的 datetime 对象
        :param tz: 目标时区
        :return: 本地时间的 datetime 对象（aware）
        """
        tzinfo = TimeZoneUtil.get_timezone(tz)
        
        if dt.tzinfo is None:
            # 假设是 UTC
            dt = dt.replace(tzinfo=TimeZoneUtil.UTC)
        
        return dt.astimezone(tzinfo)
    
    @staticmethod
    def get_utc_offset_hours(dt, tz=None):
        """
        获取指定时间点的 UTC 偏移小时数
        
        :param dt: datetime 对象
        :param tz: 时区
        :return: UTC 偏移小时数（如 +8, -5 等）
        """
        tzinfo = TimeZoneUtil.get_timezone(tz)
        
        if dt.tzinfo is None:
            if HAS_PYTZ and hasattr(tzinfo, 'localize'):
                aware_dt = tzinfo.localize(dt)
            else:
                aware_dt = dt.replace(tzinfo=tzinfo)
        else:
            aware_dt = dt.astimezone(tzinfo)
        
        offset = aware_dt.utcoffset()
        if offset is None:
            return 8.0  # 默认北京时间
        
        return offset.total_seconds() / 3600
    
    @staticmethod
    def get_offset_fraction(dt, tz=None):
        """
        获取指定时间点的 UTC 偏移（以天为单位的小数）
        
        用于替换 ShouXingUtil.ONE_THIRD 的硬编码值。
        北京时间 +8 小时 = 8/24 = 1/3 天
        
        :param dt: datetime 对象
        :param tz: 时区
        :return: UTC 偏移（天）
        """
        hours = TimeZoneUtil.get_utc_offset_hours(dt, tz)
        return hours / 24.0
    
    @staticmethod
    def is_dst(dt, tz=None):
        """
        检查指定时间是否处于夏令时
        
        :param dt: datetime 对象
        :param tz: 时区
        :return: True 如果处于夏令时，否则 False
        """
        tzinfo = TimeZoneUtil.get_timezone(tz)
        
        if dt.tzinfo is None:
            if HAS_PYTZ and hasattr(tzinfo, 'localize'):
                aware_dt = tzinfo.localize(dt)
            else:
                aware_dt = dt.replace(tzinfo=tzinfo)
        else:
            aware_dt = dt.astimezone(tzinfo)
        
        dst = aware_dt.dst()
        return dst is not None and dst.total_seconds() > 0
    
    @staticmethod
    def datetime_to_ymdhms(dt, tz=None):
        """
        将 datetime 转换为年月日时分秒元组（使用指定时区）
        
        如果 dt 是 naive 的，按指定时区（或默认时区）解释。
        如果 dt 是 aware 的，先转换到指定时区。
        
        :param dt: datetime 对象
        :param tz: 目标时区
        :return: (year, month, day, hour, minute, second) 元组
        """
        tzinfo = TimeZoneUtil.get_timezone(tz)
        
        if dt.tzinfo is not None:
            # aware datetime，转换到目标时区
            local_dt = dt.astimezone(tzinfo)
        else:
            # naive datetime，直接按目标时区解释
            local_dt = dt
        
        return (local_dt.year, local_dt.month, local_dt.day,
                local_dt.hour, local_dt.minute, local_dt.second)
    
    @staticmethod
    def ymdhms_to_datetime(year, month, day, hour, minute, second, tz=None):
        """
        从年月日时分秒创建 datetime 对象
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param hour: 时
        :param minute: 分
        :param second: 秒
        :param tz: 时区
        :return: 带时区的 datetime 对象
        """
        dt = datetime(year, month, day, hour, minute, second)
        tzinfo = TimeZoneUtil.get_timezone(tz)
        
        if HAS_PYTZ and hasattr(tzinfo, 'localize'):
            return tzinfo.localize(dt)
        else:
            return dt.replace(tzinfo=tzinfo)
    
    @staticmethod
    def has_full_tz_support():
        """
        检查是否有完整的时区支持
        
        :return: True 如果有 zoneinfo 或 pytz 支持
        """
        return ZoneInfo is not None or HAS_PYTZ
    
    # ==================== 真太阳时计算 ====================
    
    # 常用城市经度（东经为正，西经为负）
    CITY_LONGITUDES = {
        # 中国主要城市
        "北京": 116.4,
        "上海": 121.5,
        "广州": 113.3,
        "深圳": 114.1,
        "成都": 104.1,
        "重庆": 106.5,
        "武汉": 114.3,
        "西安": 108.9,
        "杭州": 120.2,
        "南京": 118.8,
        "天津": 117.2,
        "沈阳": 123.4,
        "哈尔滨": 126.6,
        "乌鲁木齐": 87.6,
        "拉萨": 91.1,
        "香港": 114.2,
        "台北": 121.5,
        "澳门": 113.5,
        
        # 国际主要城市
        "Tokyo": 139.7,       # 东京
        "Seoul": 127.0,       # 首尔
        "Singapore": 103.8,   # 新加坡
        "London": -0.1,       # 伦敦
        "Paris": 2.3,         # 巴黎
        "Berlin": 13.4,       # 柏林
        "Moscow": 37.6,       # 莫斯科
        "New York": -74.0,    # 纽约
        "Los Angeles": -118.2, # 洛杉矶
        "Chicago": -87.6,     # 芝加哥
        "Sydney": 151.2,      # 悉尼
        "Melbourne": 145.0,   # 墨尔本
        "Vancouver": -123.1,  # 温哥华
        "Toronto": -79.4,     # 多伦多
        "Dubai": 55.3,        # 迪拜
    }
    
    # 时区标准子午线经度
    TIMEZONE_MERIDIANS = {
        "Asia/Shanghai": 120,      # 东八区，120°E
        "Asia/Tokyo": 135,         # 东九区，135°E
        "Asia/Seoul": 135,         # 韩国标准时间，135°E
        "Asia/Singapore": 105,     # 新加坡（实际用UTC+8但地理上接近UTC+7）
        "Asia/Hong_Kong": 120,     # 香港，120°E
        "Asia/Taipei": 120,        # 台北，120°E
        "Europe/London": 0,        # 格林威治，0°
        "Europe/Paris": 15,        # 中欧时间，15°E
        "Europe/Berlin": 15,       # 中欧时间，15°E
        "Europe/Moscow": 45,       # 莫斯科时间，45°E
        "America/New_York": -75,   # 美东时间，75°W
        "America/Chicago": -90,    # 美中时间，90°W
        "America/Denver": -105,    # 山地时间，105°W
        "America/Los_Angeles": -120, # 美西时间，120°W
        "Australia/Sydney": 150,   # 澳东时间，150°E
        "Pacific/Auckland": 180,   # 新西兰时间，180°
    }
    
    @staticmethod
    def get_day_of_year(year, month, day):
        """
        计算一年中的第几天
        
        :param year: 年
        :param month: 月
        :param day: 日
        :return: 一年中的第几天 (1-366)
        """
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # 闰年判断
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_month[2] = 29
        
        day_of_year = sum(days_in_month[:month]) + day
        return day_of_year
    
    @staticmethod
    def equation_of_time(day_of_year):
        """
        计算时差方程（Equation of Time）
        
        时差方程描述了真太阳时与平太阳时之间的差异，
        主要由地球轨道的椭圆形和地轴倾斜引起。
        
        :param day_of_year: 一年中的第几天
        :return: 时差（分钟），正值表示真太阳时快于平太阳时
        """
        # B = 360/365 * (d - 81)，其中d是一年中的天数
        B = math.radians(360.0 / 365.0 * (day_of_year - 81))
        
        # 时差方程近似公式（单位：分钟）
        # EoT = 9.87 * sin(2B) - 7.53 * cos(B) - 1.5 * sin(B)
        eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
        
        return eot
    
    @staticmethod
    def get_longitude(location):
        """
        获取地点的经度
        
        :param location: 地点名称或经度值
            - str: 城市名称（如 "北京", "上海", "New York"）
            - float/int: 经度值（东经为正，西经为负）
        :return: 经度值
        :raises ValueError: 未知的城市名称
        """
        if isinstance(location, (int, float)):
            return float(location)
        
        if location in TimeZoneUtil.CITY_LONGITUDES:
            return TimeZoneUtil.CITY_LONGITUDES[location]
        
        raise ValueError(f"未知的城市名称: {location}. 请直接提供经度值（东经为正，西经为负）")
    
    @staticmethod
    def get_standard_meridian(tz=None):
        """
        获取时区的标准子午线经度
        
        :param tz: 时区名称
        :return: 标准子午线经度
        """
        if tz is None:
            tz = TimeZoneUtil.DEFAULT_TIMEZONE
        
        if isinstance(tz, str) and tz in TimeZoneUtil.TIMEZONE_MERIDIANS:
            return TimeZoneUtil.TIMEZONE_MERIDIANS[tz]
        
        # 根据UTC偏移估算标准子午线
        try:
            tzinfo = TimeZoneUtil.get_timezone(tz)
            # 使用一个非DST时间点来获取标准偏移
            test_dt = datetime(2020, 1, 1, 12, 0, 0)
            if HAS_PYTZ and hasattr(tzinfo, 'localize'):
                aware_dt = tzinfo.localize(test_dt)
            else:
                aware_dt = test_dt.replace(tzinfo=tzinfo)
            offset_hours = aware_dt.utcoffset().total_seconds() / 3600
            return offset_hours * 15  # 每小时对应15度经度
        except:
            return 120  # 默认北京时间标准子午线
    
    @staticmethod
    def local_mean_time_offset(longitude, tz=None):
        """
        计算地方平时与标准时间的偏移
        
        :param longitude: 当地经度（东经为正，西经为负）
        :param tz: 时区
        :return: 偏移分钟数（正值表示当地时间快于标准时间）
        """
        standard_meridian = TimeZoneUtil.get_standard_meridian(tz)
        
        # 每度经度差对应4分钟时差
        offset_minutes = (longitude - standard_meridian) * 4
        
        return offset_minutes
    
    @staticmethod
    def true_solar_time_offset(year, month, day, longitude, tz=None):
        """
        计算真太阳时与标准时间的总偏移
        
        真太阳时 = 标准时间 + 地方平时偏移 + 时差方程
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param longitude: 当地经度
        :param tz: 时区
        :return: 偏移分钟数
        """
        # 地方平时偏移
        lmt_offset = TimeZoneUtil.local_mean_time_offset(longitude, tz)
        
        # 时差方程
        day_of_year = TimeZoneUtil.get_day_of_year(year, month, day)
        eot = TimeZoneUtil.equation_of_time(day_of_year)
        
        # 总偏移 = 地方平时偏移 + 时差方程
        total_offset = lmt_offset + eot
        
        return total_offset
    
    @staticmethod
    def to_true_solar_time(dt, longitude, tz=None):
        """
        将标准时间转换为真太阳时
        
        :param dt: datetime 对象（标准时间）
        :param longitude: 当地经度（可以是城市名或经度值）
        :param tz: 时区
        :return: 真太阳时的 datetime 对象
        """
        # 获取经度
        lon = TimeZoneUtil.get_longitude(longitude)
        
        # 计算偏移
        offset_minutes = TimeZoneUtil.true_solar_time_offset(
            dt.year, dt.month, dt.day, lon, tz
        )
        
        # 应用偏移
        true_solar_dt = dt + timedelta(minutes=offset_minutes)
        
        return true_solar_dt
    
    @staticmethod
    def from_true_solar_time(dt, longitude, tz=None):
        """
        将真太阳时转换为标准时间
        
        :param dt: datetime 对象（真太阳时）
        :param longitude: 当地经度（可以是城市名或经度值）
        :param tz: 时区
        :return: 标准时间的 datetime 对象
        """
        # 获取经度
        lon = TimeZoneUtil.get_longitude(longitude)
        
        # 计算偏移（反向）
        offset_minutes = TimeZoneUtil.true_solar_time_offset(
            dt.year, dt.month, dt.day, lon, tz
        )
        
        # 反向应用偏移
        standard_dt = dt - timedelta(minutes=offset_minutes)
        
        return standard_dt
    
    @staticmethod
    def get_true_solar_time_info(year, month, day, hour, minute, longitude, tz=None):
        """
        获取真太阳时详细信息
        
        :param year: 年
        :param month: 月
        :param day: 日
        :param hour: 时
        :param minute: 分
        :param longitude: 当地经度
        :param tz: 时区
        :return: dict 包含详细信息
        """
        lon = TimeZoneUtil.get_longitude(longitude)
        standard_meridian = TimeZoneUtil.get_standard_meridian(tz)
        day_of_year = TimeZoneUtil.get_day_of_year(year, month, day)
        
        lmt_offset = TimeZoneUtil.local_mean_time_offset(lon, tz)
        eot = TimeZoneUtil.equation_of_time(day_of_year)
        total_offset = lmt_offset + eot
        
        # 计算真太阳时
        standard_dt = datetime(year, month, day, hour, minute, 0)
        true_solar_dt = standard_dt + timedelta(minutes=total_offset)
        
        return {
            "standard_time": standard_dt,
            "true_solar_time": true_solar_dt,
            "longitude": lon,
            "standard_meridian": standard_meridian,
            "longitude_offset_minutes": lmt_offset,
            "equation_of_time_minutes": round(eot, 2),
            "total_offset_minutes": round(total_offset, 2),
            "day_of_year": day_of_year,
        }
