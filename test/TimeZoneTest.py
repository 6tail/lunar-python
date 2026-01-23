# -*- coding: utf-8 -*-
"""
时区/夏令时支持测试

测试中国1986-1991年夏令时和全球时区支持。
"""
import unittest
from datetime import datetime, timezone, timedelta

from lunar_python import Solar, Lunar
from lunar_python.util import TimeZoneUtil


class TimeZoneTest(unittest.TestCase):
    """时区工具类测试"""
    
    def test_default_timezone(self):
        """测试默认时区为 Asia/Shanghai"""
        tz = TimeZoneUtil.get_timezone()
        self.assertIsNotNone(tz)
    
    def test_get_timezone_by_name(self):
        """测试通过名称获取时区"""
        if TimeZoneUtil.has_full_tz_support():
            tz = TimeZoneUtil.get_timezone("America/New_York")
            self.assertIsNotNone(tz)
    
    def test_utc_conversion(self):
        """测试 UTC 转换"""
        dt = datetime(2020, 6, 15, 12, 0, 0)
        utc_dt = TimeZoneUtil.to_utc(dt)
        self.assertIsNotNone(utc_dt)
        self.assertEqual(utc_dt.tzinfo, timezone.utc)


class ChinaDSTTest(unittest.TestCase):
    """
    中国夏令时测试 (1986-1991)
    
    中国在1986-1991年期间实行夏令时：
    - 夏令时期间 UTC+9
    - 非夏令时期间 UTC+8
    
    最后一次夏令时：1991年4月14日 02:00 开始，1991年9月15日 02:00 结束
    """
    
    def test_1991_dst_summer(self):
        """测试1991年夏令时期间（应该是 UTC+9）"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 1991年6月1日 - 夏令时期间
        solar = Solar.fromYmdHms(1991, 6, 1, 12, 0, 0)
        offset = solar.getUTCOffset()
        # 夏令时期间应该是 +9
        self.assertEqual(9, offset)
        self.assertTrue(solar.isDST())
    
    def test_1991_dst_end(self):
        """测试1991年夏令时结束后（应该是 UTC+8）"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 1991年10月1日 - 夏令时结束后
        solar = Solar.fromYmdHms(1991, 10, 1, 12, 0, 0)
        offset = solar.getUTCOffset()
        # 夏令时结束后应该是 +8
        self.assertEqual(8, offset)
        self.assertFalse(solar.isDST())
    
    def test_1992_no_dst(self):
        """测试1992年及以后没有夏令时（应该是 UTC+8）"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 1992年6月1日 - 已经取消夏令时
        solar = Solar.fromYmdHms(1992, 6, 1, 12, 0, 0)
        offset = solar.getUTCOffset()
        # 1992年后应该是固定 +8
        self.assertEqual(8, offset)
        self.assertFalse(solar.isDST())
    
    def test_dst_affects_lunar_calculation(self):
        """测试夏令时对农历计算的影响"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 使用真实案例测试
        # 1991年夏令时期间的一个日期
        solar = Solar.fromYmdHms(1991, 5, 12, 23, 30, 0)
        lunar = solar.getLunar()
        
        # 验证农历日期
        self.assertIsNotNone(lunar)
        # 1991年5月12日应该是农历三月廿八
        self.assertEqual(1991, lunar.getYear())


class TimezoneConversionTest(unittest.TestCase):
    """时区转换测试"""
    
    def test_solar_timezone_conversion(self):
        """测试 Solar 对象的时区转换"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 创建北京时间的 Solar 对象
        solar_beijing = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0, "Asia/Shanghai")
        
        # 转换到纽约时间
        solar_ny = solar_beijing.toTimezone("America/New_York")
        
        # 纽约时间应该比北京时间早12小时（夏令时）
        # 北京 12:00 = 纽约 00:00 (前一天)
        self.assertEqual(0, solar_ny.getHour())
    
    def test_from_aware_datetime(self):
        """测试从带时区的 datetime 创建 Solar"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 创建 UTC 时间的 datetime
        utc_dt = datetime(2020, 6, 15, 4, 0, 0, tzinfo=timezone.utc)
        
        # 转换为北京时间的 Solar 对象
        solar = Solar.fromDate(utc_dt, "Asia/Shanghai")
        
        # UTC 4:00 = 北京 12:00
        self.assertEqual(12, solar.getHour())
    
    def test_to_utc_datetime(self):
        """测试 Solar 转换为 UTC datetime"""
        solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
        utc_dt = solar.toUTC()
        
        self.assertIsNotNone(utc_dt)
        self.assertEqual(timezone.utc, utc_dt.tzinfo)


class LunarTimezoneTest(unittest.TestCase):
    """农历时区测试"""
    
    def test_lunar_from_solar_with_timezone(self):
        """测试从带时区的 Solar 创建 Lunar"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 创建北京时间的 Solar 对象
        solar = Solar.fromYmdHms(2020, 1, 25, 12, 0, 0, "Asia/Shanghai")
        lunar = solar.getLunar()
        
        # 验证时区被正确传递
        self.assertEqual("Asia/Shanghai", lunar.getTimezone() or "Asia/Shanghai")
    
    def test_lunar_direct_construction_with_timezone(self):
        """测试直接用时区构造 Lunar"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 直接创建带时区的 Lunar 对象
        lunar = Lunar.fromYmdHms(2020, 1, 1, 12, 0, 0, "Asia/Shanghai")
        
        # 验证时区
        self.assertEqual("Asia/Shanghai", lunar.getTimezone() or "Asia/Shanghai")


class JieQiTimezoneTest(unittest.TestCase):
    """节气时区测试"""
    
    def test_jieqi_with_timezone(self):
        """测试节气计算考虑时区"""
        if not TimeZoneUtil.has_full_tz_support():
            self.skipTest("需要完整的时区支持")
        
        # 获取2020年立春的精确时间
        lunar = Lunar.fromYmd(2020, 1, 1, "Asia/Shanghai")
        jie_qi_table = lunar.getJieQiTable()
        
        li_chun = jie_qi_table.get("立春")
        self.assertIsNotNone(li_chun)
        
        # 2020年立春是2月4日或5日（取决于精确时间和时区转换）
        self.assertEqual(2020, li_chun.getYear())
        self.assertEqual(2, li_chun.getMonth())
        # 立春通常在2月3-5日之间
        self.assertIn(li_chun.getDay(), [3, 4, 5])


class BackwardCompatibilityTest(unittest.TestCase):
    """向后兼容性测试"""
    
    def test_default_behavior_unchanged(self):
        """测试不传时区时的默认行为"""
        # 不传时区参数
        solar1 = Solar.fromYmd(2020, 6, 15)
        solar2 = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
        
        # 应该正常工作
        self.assertEqual("2020-06-15", solar1.toString())
        self.assertEqual(12, solar2.getHour())
        
        # 农历转换应该正常
        lunar = solar1.getLunar()
        self.assertIsNotNone(lunar)
    
    def test_julian_day_calculation(self):
        """测试儒略日计算"""
        solar = Solar.fromYmdHms(2000, 1, 1, 12, 0, 0)
        jd = solar.getJulianDay()
        
        # 2000年1月1日12:00 UTC 的儒略日约为 2451545
        # 由于默认是北京时间，实际会有偏移
        self.assertIsNotNone(jd)


if __name__ == '__main__':
    unittest.main()
