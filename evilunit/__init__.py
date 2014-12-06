# -*- coding:utf-8 -*-
import pkg_resources


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
