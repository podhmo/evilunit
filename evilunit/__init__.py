# -*- coding:utf-8 -*-
import pkg_resources
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


def paramaterized(candidates):
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
