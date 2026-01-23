# -*- coding: utf-8 -*-
"""
自定义异常类

提供更语义化的异常类型，便于用户捕获和处理特定错误。
"""


class LunarException(Exception):
    """
    lunar_python 库的基础异常类
    
    所有自定义异常都继承自此类，用户可以用它来捕获所有库相关的异常。
    """
    pass


class DateException(LunarException):
    """
    日期相关异常的基类
    """
    pass


class SolarDateException(DateException):
    """
    阳历日期异常
    
    当创建 Solar 对象时传入非法的年、月、日、时、分、秒时抛出。
    
    示例：
        - Solar.fromYmd(2020, 2, 30)  # 2月没有30日
        - Solar.fromYmd(2020, 13, 1)  # 月份超出范围
        - Solar.fromYmd(1582, 10, 10) # 儒略历空白期
    """
    pass


class LunarDateException(DateException):
    """
    农历日期异常
    
    当创建 Lunar 对象时传入非法的农历年、月、日时抛出。
    
    示例：
        - Lunar.fromYmd(2020, 13, 1)  # 不存在的农历月
        - Lunar.fromYmd(2020, 1, 31)  # 该月没有31日
    """
    pass
