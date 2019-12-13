import pytest


def dependency(f=None, depends=None):
    if f is None:
        return lambda f: dependency(f, depends)

    name = f.__name__.strip('test_')
    return pytest.mark.dependency(name=name, depends=depends)(f)
