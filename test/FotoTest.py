# -*- coding: utf-8 -*-
import unittest
from lunar_python import Foto, Lunar


class FotoTest(unittest.TestCase):
    def test(self):
        foto = Foto.fromLunar(Lunar.fromYmd(2021, 10, 14))
        self.assertEqual("二五六五年十月十四 (三元降) (四天王巡行)", foto.toFullString())
