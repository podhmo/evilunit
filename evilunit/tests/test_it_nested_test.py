# -*- coding:utf-8 -*-
import unittest
from evilunit import NestedTest, nested_test_compile


@nested_test_compile
class SelfTest(NestedTest):
    @classmethod
    def setUpClass(cls):
        assert issubclass(cls, unittest.TestCase)
        cls.L = ["t1"]

    def setUp(self):
        assert isinstance(self, unittest.TestCase)
        self.L.append("t2")

    def test_it(self):
        assert isinstance(self, unittest.TestCase)
        self.L.append("t3")

    def tearDown(self):
        assert isinstance(self, unittest.TestCase)
        self.L.append("t4")

    @classmethod
    def tearDownClass(cls):
        assert issubclass(cls, unittest.TestCase)
        assert cls.L == ["t1", "t2", "t3", "t4"]


L = []


@nested_test_compile
class ToplevelTest(NestedTest):
    @classmethod
    def setUpClass(cls):
        assert issubclass(cls, unittest.TestCase)
        L.append("t1")

    def setUp(self):
        assert isinstance(self, unittest.TestCase)
        L.append("t2")

    def test_it(self):
        assert isinstance(self, unittest.TestCase)
        L.append("t3")
        self.assertEqual(L, ["t1", "t2", "t3"])

    def tearDown(self):
        assert isinstance(self, unittest.TestCase)
        global L
        L = []

    class Child(NestedTest):
        @classmethod
        def setUpClass(cls):
            assert issubclass(cls, unittest.TestCase)
            L.append("m1")

        def setUp(self):
            assert isinstance(self, unittest.TestCase)
            L.append("m2")

        def test_it(self):
            assert isinstance(self, unittest.TestCase)
            L.append("m3")
            self.assertEqual(L, ["t1", "m1", "t2", "m2", "m3"])

        class GrandChild(NestedTest):
            @classmethod
            def setUpClass(cls):
                assert issubclass(cls, unittest.TestCase)
                L.append("n1")

            def setUp(self):
                assert isinstance(self, unittest.TestCase)
                L.append("n2")

            def test_it(self):
                assert isinstance(self, unittest.TestCase)
                L.append("n3")
                self.assertEqual(L, ["t1", "m1", "n1", "t2", "m2", "n2", "n3"])

    class Child2(NestedTest):
        @classmethod
        def setUpClass(cls):
            assert issubclass(cls, unittest.TestCase)
            L.append("o1")

        def setUp(self):
            assert isinstance(self, unittest.TestCase)
            L.append("o2")

        def test_it(self):
            assert isinstance(self, unittest.TestCase)
            L.append("o3")
            self.assertEqual(L, ["t1", "o1", "t2", "o2", "o3"])
