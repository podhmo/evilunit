i = 0


def gensym():
    global i
    i += 1
    return "G{}".format(i)


import sys


def parameterized(candidates):
    # candidates = [(args, ..., expected)]

    def _parameterize(method):
        env = sys._getframe(1).f_locals  # xxx
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
