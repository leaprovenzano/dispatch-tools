import pytest

from dispatchtools import directdispatch
from dispatchtools.exceptions import InvalidCallableError


def test_invalid_default_raises_error():

    with pytest.raises(InvalidCallableError):

        @directdispatch
        def func():
            return 'default'


def test_invalid_register_raises_error():
    @directdispatch
    def func(*args, **kwargs):
        return 'default'

    with pytest.raises(InvalidCallableError):

        @func.register(1)
        def _():
            return 'crap'


def test_basic_dispatcher():
    @directdispatch
    def func(*args, **kwargs):
        return 'default'

    @func.register(1)
    def _(a):
        return 'one'

    @func.register(2)
    def _(a, b='x'):
        return 'two'

    assert func(1) == 'one'
    assert func(2) == 'two'
    assert func(2, b=10) == 'two'
    assert func(3) == 'default'


def test_stacking_decorator():
    @directdispatch
    def func(*args, **kwargs):
        return 'default'

    @func.register(1)
    @func.register('one')
    def _(a):
        return 'one'

    assert func(1) == 'one'
    assert func('one') == 'one'
    assert func(2) == 'default'


def test_basic_bound_dispatcher():
    class MyCls:

        @directdispatch
        def func(self, *args, **kwargs):
            return 'default'

        @func.register(1)
        def _(self, a):
            return 'one'

        @func.register(2)
        def _(self, a, b='x'):
            return 'two'

    inst = MyCls()
    assert inst.func(1) == 'one'
    assert inst.func(2) == 'two'
    assert inst.func(2, b=10) == 'two'
    assert inst.func(3) == 'default'


def test_stacking_bound_decorator():
    class MyCls:

        @directdispatch
        def func(self, *args, **kwargs):
            return 'default'

        @func.register(1)
        @func.register('one')
        def _(self, a):
            return 'one'

    inst = MyCls()
    assert inst.func(1) == 'one'
    assert inst.func('one') == 'one'
    assert inst.func(3) == 'default'
