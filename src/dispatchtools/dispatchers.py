from typing import Hashable, Callable, Optional
from dispatchtools._abcs import Dispatcher

from dispatchtools.registry import Registry


class directdispatch(Dispatcher):  # noqa: N801

    """The simplest kind of dispatch based on exact values.

    Example:

        >>> from dispatchtools import directdispatch
        >>>
        >>> @directdispatch
        ... def myfunc(n):
        ...     return 'something else'
        ...
        >>> @myfunc.register(2)
        ... def _(n):
        ...     return 'two'
        ...
        >>> @myfunc.register(3)
        ... def _(n):
        ...     return 'three'
        ...
        >>> myfunc(1)
        'something else'
        >>> myfunc(2)
        'two'
        >>> myfunc(3)
        'three'
    """

    def __init__(self, f: Callable):
        self.__default__ = f
        self._name = f.__name__
        self.registry = Registry()

    def register(self, value: Hashable, f: Optional[Callable] = None) -> Callable:
        if f is None:
            return lambda f: self.register(value, f)
        self.registry.register(value, f)
        return f

    def __dispatch__(self, *args, **kwargs) -> Callable:
        return self.registry.get(args[0], self.__default__)
