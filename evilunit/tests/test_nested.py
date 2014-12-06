# -*- coding:utf-8 -*-
import unittest


class NestedSelfTests(unittest.TestCase):
    def _getTarget(self):
        from evilunit import NestedTestCompiler
        return NestedTestCompiler

    def _makeOne(self, L):
        from evilunit import NestedTest

        class Toplevel(NestedTest):
            @classmethod
            def setUpClass(self):
                assert issubclass(self, unittest.TestCase)
                L.append("t1")

            def setUp(self):
                assert isinstance(self, unittest.TestCase)
                L.append("t2")

            def test_it(self):
                assert isinstance(self, unittest.TestCase)
                L.append("t3")

            def tearDown(self):
                assert isinstance(self, unittest.TestCase)
                L.append("t4")

            @classmethod
            def tearDownClass(self):
                assert issubclass(self, unittest.TestCase)
                L.append("t5")
        return self._getTarget()(Toplevel)

    def test_setUpClass(self):
        L = []
        target = self._makeOne(L)
        TestCase = target.compile()
        TestCase.setUpClass()
        self.assertEqual(L, ["t1"])

    def test_setUp(self):
        L = []
        target = self._makeOne(L)
        TestCase = target.compile()
        TestCase().setUp()
        self.assertEqual(L, ["t2"])

    def test_tearDown(self):
        L = []
        target = self._makeOne(L)
        TestCase = target.compile()
        TestCase().tearDown()
        self.assertEqual(L, ["t4"])

    def test_tearDownClass(self):
        L = []
        target = self._makeOne(L)
        TestCase = target.compile()
        TestCase.tearDownClass()
        self.assertEqual(L, ["t5"])

    def test_it(self):
        L = []
        target = self._makeOne(L)
        TestCase = target.compile()
        TestCase().test_it()
        self.assertEqual(L, ["t3"])


class NestedDoesNotInterfereEachSibbilngTests(unittest.TestCase):
    def _getTarget(self):
        from evilunit import NestedTestCompiler
        return NestedTestCompiler

    def _makeOne(self, L):
        from evilunit import NestedTest

        class Toplevel(NestedTest):
            @classmethod
            def setUpClass(self):
                assert issubclass(self, unittest.TestCase)
                L.append("t1")

            def setUp(self):
                assert isinstance(self, unittest.TestCase)
                L.append("t2")

            class Child0(NestedTest):
                @classmethod
                def setUpClass(self):
                    assert issubclass(self, unittest.TestCase)
                    L.append("m1")

                def setUp(self):
                    assert isinstance(self, unittest.TestCase)
                    L.append("m2")

            class Child1(NestedTest):
                @classmethod
                def setUpClass(self):
                    assert issubclass(self, unittest.TestCase)
                    L.append("n1")

                def setUp(self):
                    assert isinstance(self, unittest.TestCase)
                    L.append("n2")

        return self._getTarget()(Toplevel)

    def test_setUpClass(self):
        L = []
        target = self._makeOne(L)
        target.compile()
        child = [c for c in target.children if c.name == "Nested_Toplevel_Child0"][0]
        child.compile().setUpClass()
        self.assertEqual(L, ["t1", "m1"])

    def test_setUp(self):
        L = []
        target = self._makeOne(L)
        target.compile()
        child = [c for c in target.children if c.name == "Nested_Toplevel_Child0"][0]
        child.compile()().setUp()
        self.assertEqual(L, ["t2", "m2"])


class NestedParentsOrderTests(unittest.TestCase):
    def _getTarget(self):
        from evilunit import NestedTestCompiler
        return NestedTestCompiler

    def _makeOne(self, L):
        from evilunit import NestedTest

        class Toplevel(NestedTest):
            @classmethod
            def setUpClass(self):
                L.append("t1")

            def setUp(self):
                L.append("t2")

            class Child0(NestedTest):
                @classmethod
                def setUpClass(self):
                    L.append("m1")

                def setUp(self):
                    L.append("m2")

                class Child1(NestedTest):
                    @classmethod
                    def setUpClass(self):
                        L.append("n1")

                    def setUp(self):
                        L.append("n2")

        return self._getTarget()(Toplevel)

    def test_setUpClass(self):
        L = []
        target = self._makeOne(L)
        target.compile()
        grand_child = target.children[0].children[0]
        grand_child.compile().setUpClass()
        self.assertEqual(L, ["t1", "m1", "n1"])

    def test_setUp(self):
        L = []
        target = self._makeOne(L)
        target.compile()
        grand_child = target.children[0].children[0]
        grand_child.compile()().setUp()
        self.assertEqual(L, ["t2", "m2", "n2"])
