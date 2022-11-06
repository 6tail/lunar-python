# -*- coding: utf-8 -*-
import unittest


class ChineseTest(unittest.TestCase):
    def test(self):
        gz = "甲午"
        g = gz[:1]
        z = gz[1:]
        print(g)
        print(z)
        self.assertEqual("甲", g)
        self.assertEqual("午", z)
