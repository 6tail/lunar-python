# -*- coding: utf-8 -*-
import unittest
from lunar_python import Solar, Lunar


class NineStarTest(unittest.TestCase):

    def test1(self):
        lunar = Solar.fromYmd(1985, 2, 19).getLunar()
        self.assertEqual("六", lunar.getYearNineStar().getNumber())

    def test23(self):
        lunar = Lunar.fromYmd(2022, 1, 1)
        self.assertEqual('六白金开阳', lunar.getYearNineStar().toString())

    def test24(self):
        lunar = Lunar.fromYmd(2033, 1, 1)
        self.assertEqual('四绿木天权', lunar.getYearNineStar().toString())
