from typing import Hashable, Callable, Optional
from types import DynamicClassAttribute
import functools

from abc import ABC, abstractmethod

from dispatchtools.utils import accepts_args
from dispatchtools.exceptions import InvalidCallableError


class Dispatcher(ABC):

    """Abstract Base class for dispatchers.

    All dispatchers should inherit from Dispatcher and define the following methods:

        - register
        - __dispatch__
    """

    def validate_callable(self, f: Callable):
        """Raise an error if callable cannot be used in dispatch otherwise do nothing.

        The dispatcher base class simply checks that function passed in can
        accept arguements since this is the most basic requirement for a
        callable to be used in dispatch. Children of `Dispatcher` should override
        this method and call super().validate_callable() in that method to add functionality
        and maintain a stable interface.

        Raises:
            InvalidCallableError
        """
        if not accepts_args(f):
            raise InvalidCallableError(f, 'dispatch functions must accept args.')

    @DynamicClassAttribute
    def register(self) -> Callable:
        return self.__register__

    @abstractmethod
    def __register__(self, value: Hashable, f: Optional[Callable]) -> Callable:
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
