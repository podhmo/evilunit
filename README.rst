evilunit
========================================

features

- shortcuts
- parameterized
- nested

shortcuts
----------------------------------------

this is tiresome.

.. code:: python

    import unittest

    class Tests(unittest.TestCase):
        def _getTarget(self):
            from foo.bar import boo
            return boo

        def _callFUT(self, *args, **kwargs):
            self._getTarget()(*args, **kwargs)

        def test_it(self):
            params = object()
            result = self._callFUT(params)
            self.assertEqual(result, params)


shortcuts decorator

- test_target -- adding _getTarget(), _makeOne() methods
- test_function  -- adding _getTarget(), _callFUT() methods


.. code:: python

    import unittest
    from evilunit import test_function

    @test_function("foo.bar:boo")
    class Tests(unittest.TestCase):
        def test_it(self):
            params = object()
            result = self._callFUT(params)
            self.assertEqual(result, params)



parameterized
----------------------------------------

.. code:: python

    import unittest
    from evilunit import NestedTest, nested_test_compile

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
            """adding number"""
            result = self._callFUT(x, y)
            self.assertEqual(result, expected)

        @classmethod
        def tearDownClass(cls):
            count_of_test_method = sum(1 for k, v in cls.__dict__.items() if k.startswith("test_") and callable(v))
            assert count_of_test_method == 5


nested
----------------------------------------

.. code:: python

    import unittest
    from evilunit import NestedTest, nested_test_compile


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

            def tearDown(self):
                assert isinstance(self, unittest.TestCase)
                global L
                L = []

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

                def tearDown(self):
                    assert isinstance(self, unittest.TestCase)
                    global L
                    L = []

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

            def tearDown(self):
                assert isinstance(self, unittest.TestCase)
                global L
                L = []

