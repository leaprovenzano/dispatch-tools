from typing import Hashable, Callable, Optional
from types import MappingProxyType
from abc import ABC, abstractmethod


class Dispatcher(ABC):

    """Abstract Base class for dispatchers.

    All dispatchers should inherit from Dispatcher and define the following methods:

        - register
        - __dispatch__
        - __call__
    """

    def __init__(self, f: Callable):
        self._name = f.__name__
        self._default = f
        self._registry = {}

    @property
    def registry(self) -> MappingProxyType:
        """an immutable view of the dispatchers registry.
        """
        return MappingProxyType(self._registry)

    @abstractmethod
    def register(self, value: Hashable, f: Optional[Callable] = None) -> Callable:
        """register a funciton with the dispatcher.

        Args:
            value (Hashable): a hashable value
            f (Optional[Callable], optional): a callable
        """
        return NotImplemented

    @abstractmethod
    def __dispatch__(self, value):
        try:
            return self._registry[value]
        except KeyError:
            return self._default

    @abstractmethod
    def __call__(self, *args, **kwargs):
        return NotImplemented
