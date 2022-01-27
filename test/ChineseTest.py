# -*- coding: utf-8 -*-
import sys
import unittest


class ChineseTest(unittest.TestCase):
    def test(self):
        gz = '甲午'
        if sys.version_info.major > 2:
            gz_bytes = gz.encode("utf-8")
        else:
            gz_bytes = gz
        g = gz_bytes.decode('utf-8')[:1].encode('utf-8')
        z = gz_bytes.decode('utf-8')[1:].encode('utf-8')
        self.assertEqual('甲', g)
        self.assertEqual('午', z)
