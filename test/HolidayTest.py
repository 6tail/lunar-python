# -*- coding: utf-8 -*-
import unittest

from lunar_python.util import HolidayUtil


class HolidayTest(unittest.TestCase):
    def test(self):
        holiday = HolidayUtil.getHoliday(2010, 1, 1)
        self.assertEqual("元旦节", holiday.getName())

        HolidayUtil.fix(None, "20100101~000000000000000000000000000")
        holiday = HolidayUtil.getHoliday(2010, 1, 1)
        self.assertIsNone(holiday)
