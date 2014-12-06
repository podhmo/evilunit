# -*- coding:utf-8 -*-
import unittest
from evilunit import paramaterized


class Tests(unittest.TestCase):
    def _callFUT(self, x, y):
        return x + y

    @paramaterized([
        (1, 2, 3),
        (1, 1, 2),
        (1, 0, 1),
        (2, 3, 5),
        (4, 4, 8)
    ])
    def _test_add(self, x, y, expected):
        """単純な足し算の比較"""
        result = self._callFUT(x, y)
        self.assertEqual(result, expected)

    @classmethod
    def tearDownClass(cls):
        count_of_test_method = sum(1 for k, v in cls.__dict__.items() if k.startswith("test_") and callable(v))
        assert count_of_test_method == 5
