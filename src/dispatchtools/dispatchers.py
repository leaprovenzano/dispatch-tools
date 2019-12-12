from typing import Hashable, Callable, Optional
from dispatchtools._abcs import Dispatcher


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

    def register(self, value: Hashable, f: Optional[Callable] = None) -> Callable:
        if f is None:
            return lambda f: self.register(value, f)
        self._registry[value] = f
        return f

    def __dispatch__(self, value: Hashable) -> Callable:
        try:
            return self._registry[value]
        except KeyError:
            return self._default

    def __call__(self, *args, **kwargs):
        if not args:
            raise TypeError(f'{self._name} requires at least 1 positional argument')
        return self.__dispatch__(args[0])(*args, **kwargs)
