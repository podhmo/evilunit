# -*- coding:utf-8 -*-
import pkg_resources
import unittest
import sys


# short cut functions

def import_symbol(symbol):
    return pkg_resources.EntryPoint.parse("x=%s" % symbol).load(False)


class TestShortcutMaker(object):
    def __init__(self, get_target="_getTarget", make_one="_makeOne"):
        self.get_target = get_target
        self.make_one = make_one

    def __call__(self, symbol):
        def wrapper(cls):
            def _getTarget(self):
                return import_symbol(symbol)
            setattr(cls, self.get_target, _getTarget)

            def _makeOne(self, *args, **kwargs):
                return self._getTarget()(*args, **kwargs)

            if not hasattr(cls, self.make_one):
                setattr(cls, self.make_one, _makeOne)
            return cls
        return wrapper

test_target = TestShortcutMaker(get_target="_getTarget", make_one="_makeOne")
test_function = TestShortcutMaker(get_target="_getTarget", make_one="_callFUT")

# paramaterized test
i = 0


def gensym():
    global i
    i += 1
    return "G{}".format(i)


def parameterized(candidates):
    # candidates = [(args, ..., expected)]

    def _parameterize(method):
        env = sys._getframe(1).f_locals
        method_name = method.__name__
        for i, args in enumerate(candidates):
            paramaters = args[:-1]
            expected = args[-1]

            def test(self, n=i):
                return method(self, *candidates[n])

            test.__name__ = "{}_{}".format(method_name.lstrip("_"), gensym())
            doc = method.__doc__ or method_name
            test.__doc__ = "{}: args={}, expected={}".format(doc, paramaters, expected)
            env[test.__name__] = test
        return method
    return _parameterize

# typo. TODO:remove near feature.
paramaterized = parameterized


# nested test
class NestedTest(object):
    pass


class NestedTestCompiler(object):
    original_attr_names = set(NestedTest.__dict__.keys())

    def __init__(self, test_cls, name=None, bases=None, parent=None):
        assert issubclass(test_cls, NestedTest)

        self.test_cls = test_cls
        self.name = name or "Nested_{}".format(test_cls.__name__)
        self.bases = bases or (unittest.TestCase, )
        self.attrs = {}
        self.parent = parent
        self.children = []
        self.compiled = None
        self.used_fixture = {name: False for name in ["setUp", "setUpClass", "tearDown", "tearDownClass"]}

    def compile(self):
        if self.compiled is not None:
            return self.compiled

        self.inject_attributes()
        cls = type(self.name, self.bases, self.attrs)
        cls.__doc__ = self.test_cls.__doc__
        self.compiled = cls
        for c in self.children:
            c.compile()
        return cls

    def inject_attributes(self):
        itr = reversed(self.test_cls.__mro__)
        next(itr)  # skip object
        next(itr)  # skip NestedTest
        for cls in itr:
            attr_names = set(cls.__dict__.keys())
            originals = self.__class__.original_attr_names
            new_attr_names = attr_names.difference(originals)
            for name in new_attr_names:
                self.attrs[name] = self.dispatch(name, getattr(cls, name))

        if self.parent:
            for method_name, is_used in self.used_fixture.items():
                if is_used is False and self.parent.used_fixture.get(method_name, False):
                    self.used_fixture[method_name] = True
                    self.attrs[method_name] = self.parent.attrs[method_name]

    def dispatch(self, name, attr):
        if isinstance(attr, type) and issubclass(attr, NestedTest):
            return self.build_child_compiler(name, attr)
        elif name in ["setUp", "setUpClass", "tearDown", "tearDownClass"]:
            self.used_fixture[name] = True
            return self.build_wrapped_method(name, attr)
        else:
            return attr

    def build_child_compiler(self, name, test_cls):
        name = "_".join([self.name, name])
        child_compiler = self.__class__(test_cls, name=name, bases=self.bases, parent=self)
        self.children.append(child_compiler)
        return None  # xxx

    def build_wrapped_method(self, name, target_method):
        is_class_method = False
        doc = target_method.__doc__

        if hasattr(target_method, "__func__"):  # TODO: python2.x
            is_class_method = True
            target_method = target_method.__func__

        def wrapper(test_self):
            if self.parent is not None:
                method = getattr(self.parent.compiled, name, None)
                if method is not None and callable(method):
                    if is_class_method:
                        method()
                    else:
                        method(test_self)
            target_method(test_self)

        if is_class_method:
            wrapper = classmethod(wrapper)
        wrapper.__doc__ = doc
        return wrapper


def collect_compiled_testcase(cls):
    compiler = NestedTestCompiler(cls)
    compiler.compile()

    def walk(compiler):
        yield compiler
        for c in compiler.children:
            for gc in walk(c):
                yield gc

    for c in walk(compiler):
        if any(k.startswith("test_") for k in c.compiled.__dict__.keys()):
            yield c.compiled


def nested_test_compile(cls):
    r = collect_compiled_testcase(cls)
    env = sys._getframe(1).f_locals
    for testcase in r:
        env[testcase.__name__] = testcase
    return cls
