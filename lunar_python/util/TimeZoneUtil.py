# -*- coding: utf-8 -*-
"""
时区工具类 - 支持全球时区/夏令时历史规则

支持 IANA 时区名称（如 "Asia/Shanghai", "America/New_York"）和 tzinfo 对象。
默认时区为 Asia/Shanghai，包含中国1986-1991年夏令时历史规则。
"""

import sys
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
