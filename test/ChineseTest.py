# -*- coding: utf-8 -*-
import unittest


class ChineseTest(unittest.TestCase):
    def test(self):
        gz = '甲午'
        g = gz.decode('utf-8')[:1].encode('utf-8')
        z = gz.decode('utf-8')[1:].encode('utf-8')
        self.assertEqual('甲', g)
        self.assertEqual('午', z)
