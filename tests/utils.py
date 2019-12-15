import re
from typing import Optional
from contextlib import contextmanager
import pytest


def dependency(f=None, depends=None):
    if f is None:
        return lambda f: dependency(f, depends)

    name = f.__name__.strip('test_')
    return pytest.mark.dependency(name=name, depends=depends)(f)


@contextmanager
def not_raises(exception: Exception, match: Optional[str] = None):
    try:
        yield
    except exception as exc:
        if match is not None:
            m = re.match(match, str(exc))
            if m is None:
                raise
        else:
            raise pytest.fail("DID RAISE {0}".format(exception))
