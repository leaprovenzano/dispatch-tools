from typing import Hashable, Callable, Optional

import functools

from abc import ABC, abstractmethod


from dispatchtools.registry import Registry


class Dispatcher(ABC):

    """Abstract Base class for dispatchers.

    All dispatchers should inherit from Dispatcher and define the following methods:

        - register
        - __dispatch__
    """

    def __init__(self, f: Callable):
        self._name = f.__name__
        self.registry = Registry(f)

    @abstractmethod
    def register(self, value: Hashable, f: Optional[Callable]) -> Callable:
        """register a function with the dispatcher.

        Args:
            value (Hashable): a hashable value
            f (Optional[Callable], optional): a callable
        """
        return NotImplemented

    @abstractmethod
    def __dispatch__(self, *args, **kwargs) -> Callable:
        return NotImplemented

    def __call__(self, *args, _instance=None, **kwargs):
        if not args:
            raise TypeError(f'{self._name} requires at least 1 positional argument')
        f = self.__dispatch__(*args, **kwargs)
        if _instance is None:
            return f(*args, **kwargs)
        return f(_instance, *args, **kwargs)

    def __get__(self, inst, cls):
        if inst is None:
            return self
        return functools.partial(self.__call__, _instance=inst)
