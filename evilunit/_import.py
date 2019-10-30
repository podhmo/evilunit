from importlib import import_module


def import_symbol(path, *, sep=":"):
    """import symobl from <module path>:<name>"""
    if sep not in path:
        raise ValueError(f"please call with <module path>{sep}<name>") from None
    module_path, name = path.split(sep, 1)
    m = import_module(module_path)
    try:
        return getattr(m, name)
    except AttributeError:
        raise ImportError(f"{name} is not found in {module_path}") from None
