# -*- coding: utf-8 -*-
import unittest
from lunar_python import Foto, Lunar


class FotoTest(unittest.TestCase):
    def test(self):
        foto = Foto.fromLunar(Lunar.fromYmd(2021, 10, 14))
        self.assertEqual("二五六五年十月十四 (三元降) (四天王巡行)", foto.toFullString())

    def test1(self):
        foto = Foto.fromLunar(Lunar.fromYmd(2020, 4, 13))
        self.assertEqual("氐", foto.getXiu())
        self.assertEqual("土", foto.getZheng())
        self.assertEqual("貉", foto.getAnimal())
        self.assertEqual("东", foto.getGong())
        self.assertEqual("青龙", foto.getShou())
