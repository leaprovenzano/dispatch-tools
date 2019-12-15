import pytest

from dispatchtools.utils import accepts_args
from tests.utils import not_raises


class SomeClass:

    def empty_method(self):
        pass

    def method_with_arg(self, a):
        pass

    @classmethod
    def empty_classmethod(cls):
        pass

    @classmethod
    def classmethod_with_arg(cls, x):
        pass


def empty_function():
    pass


def function_with_arg(arg):
    pass


def function_with_star_args(*args):
    pass


def function_with_kwargs(**kwargs):
    pass


def function_with_args_kwargs(*args, **kwargs):
    pass


def function_with_default(boop=1):
    pass


func_params = (
    'f,',
    [
        empty_function,
        function_with_arg,
        function_with_star_args,
        function_with_kwargs,
        function_with_args_kwargs,
        function_with_default,
    ],
)

method_params = ('method,', [getattr(SomeClass, m) for m in dir(SomeClass) if not m.startswith('__')])


@pytest.mark.parametrize(*func_params, ids=lambda x: x.__name__)
def test_output_is_bool(f):
    assert isinstance(accepts_args(f), bool)


@pytest.mark.parametrize(*func_params, ids=lambda x: x.__name__)
def test_functions(f):

    if accepts_args(f):
        with not_raises(TypeError, match=r'.* positional argument.*'):
            f(1)
    else:
        with pytest.raises(TypeError, match=r'.*takes 0 positional arguments but 1 was given.*'):
            f(1)


@pytest.mark.parametrize(*method_params, ids=lambda x: x.__qualname__)
def test_methods(method):
    inst = SomeClass()
    bound = getattr(inst, method.__name__)

    if accepts_args(method):
        with not_raises(TypeError, match=r'.* positional argument.*'):
            bound(1)
    else:
        with pytest.raises(TypeError, match=r'.*takes 1 positional argument but 2 were given.*'):
            bound(1)
