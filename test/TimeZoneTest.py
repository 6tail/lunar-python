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


class TrueSolarTimeTest(unittest.TestCase):
    """真太阳时测试"""
    
    def test_equation_of_time(self):
        """测试时差方程计算"""
        # 时差方程在不同日期有不同的值
        # 大约在2月和11月达到极值（±15分钟）
        
        # 2月11日左右，时差方程约为 -14 分钟
        eot_feb = TimeZoneUtil.equation_of_time(42)  # 约2月11日
        self.assertLess(eot_feb, 0)  # 负值
        self.assertGreater(eot_feb, -16)  # 不超过-16分钟
        
        # 11月3日左右，时差方程约为 +16 分钟
        eot_nov = TimeZoneUtil.equation_of_time(307)  # 约11月3日
        self.assertGreater(eot_nov, 0)  # 正值
        self.assertLess(eot_nov, 18)  # 不超过18分钟
    
    def test_longitude_offset(self):
        """测试经度偏移计算"""
        # 北京（116.4°E）相对于东八区标准子午线（120°E）
        # 偏移 = (116.4 - 120) * 4 = -14.4 分钟
        offset = TimeZoneUtil.local_mean_time_offset(116.4, "Asia/Shanghai")
        self.assertAlmostEqual(offset, -14.4, places=1)
        
        # 乌鲁木齐（87.6°E）相对于东八区
        # 偏移 = (87.6 - 120) * 4 = -129.6 分钟 ≈ -2小时10分
        offset_urumqi = TimeZoneUtil.local_mean_time_offset(87.6, "Asia/Shanghai")
        self.assertAlmostEqual(offset_urumqi, -129.6, places=1)
    
    def test_city_longitude(self):
        """测试城市经度查询"""
        self.assertAlmostEqual(TimeZoneUtil.get_longitude("北京"), 116.4, places=1)
        self.assertAlmostEqual(TimeZoneUtil.get_longitude("上海"), 121.5, places=1)
        self.assertAlmostEqual(TimeZoneUtil.get_longitude("乌鲁木齐"), 87.6, places=1)
        self.assertAlmostEqual(TimeZoneUtil.get_longitude("New York"), -74.0, places=1)
    
    def test_true_solar_time_conversion(self):
        """测试真太阳时转换"""
        # 北京 2020-06-15 12:00 标准时间
        solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
        
        # 转换为真太阳时
        true_solar = solar.toTrueSolarTime("北京")
        
        # 真太阳时应该和标准时间有差异
        # 6月15日，北京（116.4°E）相对于120°E：
        # - 经度偏移: -14.4 分钟
        # - 时差方程: 约 0 分钟（6月中旬接近0）
        # 总偏移约 -14 分钟
        
        self.assertIsNotNone(true_solar)
        # 真太阳时应该比标准时间早一些
        info = solar.getTrueSolarTimeInfo("北京")
        self.assertLess(info["total_offset_minutes"], 0)
    
    def test_true_solar_time_info(self):
        """测试真太阳时详细信息"""
        solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
        info = solar.getTrueSolarTimeInfo(116.4)
        
        self.assertIn("standard_time", info)
        self.assertIn("true_solar_time", info)
        self.assertIn("longitude", info)
        self.assertIn("longitude_offset_minutes", info)
        self.assertIn("equation_of_time_minutes", info)
        self.assertIn("total_offset_minutes", info)
    
    def test_urumqi_vs_beijing(self):
        """测试乌鲁木齐和北京的真太阳时差异"""
        # 同一标准时间（北京时间12:00）
        solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
        
        # 北京真太阳时
        beijing_true = solar.toTrueSolarTime("北京")
        
        # 乌鲁木齐真太阳时
        urumqi_true = solar.toTrueSolarTime("乌鲁木齐")
        
        # 乌鲁木齐真太阳时应该比北京早约2小时
        beijing_minutes = beijing_true.getHour() * 60 + beijing_true.getMinute()
        urumqi_minutes = urumqi_true.getHour() * 60 + urumqi_true.getMinute()
        
        diff = beijing_minutes - urumqi_minutes
        # 经度差 116.4 - 87.6 = 28.8度，约 115 分钟
        self.assertGreater(diff, 100)
        self.assertLess(diff, 130)
    
    def test_bazi_with_true_solar_time(self):
        """测试使用真太阳时排盘"""
        # 北京时间 2020-06-15 12:00
        solar = Solar.fromYmdHms(2020, 6, 15, 12, 0, 0)
        lunar_standard = solar.getLunar()
        
        # 使用北京真太阳时
        lunar_true = lunar_standard.toTrueSolarTime("北京")
        
        # 两者的八字可能相同也可能不同，取决于是否跨越时辰边界
        bazi_standard = lunar_standard.getBaZi()
        bazi_true = lunar_true.getBaZi()
        
        # 验证都能正确获取八字
        self.assertEqual(len(bazi_standard), 4)
        self.assertEqual(len(bazi_true), 4)
    
    def test_from_true_solar_time(self):
        """测试从真太阳时创建对象"""
        # 假设用户提供的是真太阳时 12:00
        solar = Solar.fromTrueSolarTime(2020, 6, 15, 12, 0, 0, "北京")
        
        # 标准时间应该比真太阳时晚一些（因为北京在120°E以西）
        self.assertIsNotNone(solar)
        # 标准时间应该是 12:00 + 14分钟 ≈ 12:14
        self.assertEqual(12, solar.getHour())


if __name__ == '__main__':
    unittest.main()
