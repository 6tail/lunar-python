# -*- coding: utf-8 -*-
from datetime import datetime


class ExactDate:
    """
    精确日期
    """

    def __init__(self):
        pass

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return datetime(year, month, day, hour, minute, second, 0)

    @staticmethod
    def fromYmd(year, month, day):
        return ExactDate.fromYmdHms(year, month, day, 0, 0, 0)

    @staticmethod
    def fromDate(date):
        return ExactDate.fromYmdHms(date.year, date.month, date.day, date.hour, date.minute, date.second)
