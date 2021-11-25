# -*- coding: utf-8 -*-
import unittest
from lunar_python import Tao, Lunar


class TaoTest(unittest.TestCase):
    def test(self):
        tao = Tao.fromLunar(Lunar.fromYmdHms(2021, 10, 17, 18, 0, 0))
        self.assertEqual("四七一八年十月十七", tao.toString())
        self.assertEqual("道歷四七一八年，天运辛丑年，己亥月，癸酉日。十月十七日，酉時。", tao.toFullString())

    def test1(self):
        tao = Tao.fromYmd(4718, 10, 18)
        self.assertEqual("地母娘娘圣诞", tao.getFestivals()[0].toString())

        tao = Lunar.fromYmd(2021, 10, 18).getTao()
        self.assertEqual("四时会", tao.getFestivals()[1].toString())
