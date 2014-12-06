# -*- coding:utf-8 -*-
import sys
import unittest


def cls_decorator(cls):
    class Tests(unittest.TestCase):
        def test_it(self):
            result = 10 + 20
            self.assertEqual(result, 30)

    sys._getframe(1).f_locals["Tests"] = Tests
    return cls


@cls_decorator
class A(object):
    pass


if __name__ == "__main__":
    unittest.main()
