from typing import Hashable, Callable


class Registry(dict):

    """A Registry is a mostly immutable mapping of hashable to callables.

    Registry objects must be initilized with a default callable, this will be returned whenever
    a keyed callable cannot be found. Entries may only be created using the `register` method and may
    not be further modified after creation.


    Args:
        default (Callable): this implementation will be returned whenever a missing key is requested.

    """

    def __init__(self, default: Callable):
        if not callable(default):
            raise TypeError(f'{self.__class__.__name__} default must be a callable')
        self._default = default

    def register(self, key: Hashable, value: Callable = None) -> Callable:
        if key in self:
            self._on_mutation()
        if not callable(value):
            raise TypeError(f'{self.__class__.__name__} values must be callable')
        super().__setitem__(key, value)

    def __getitem__(self, key: Hashable) -> Callable:
        return super().get(key, self._default)

    def _on_mutation(self, *args, **kws):
        raise TypeError(f'{self.__class__.__name__} objects must not be further mutated creation.')

    def _on_forbidden_set(self, *args, **kws):
        raise TypeError(f'{self.__class__.__name__} entries may only be created by the register method.')

    __setitem__ = _on_forbidden_set
    __delitem__ = _on_mutation
    clear = _on_mutation
    update = _on_forbidden_set
    setdefault = _on_mutation
    pop = _on_mutation
    popitem = _on_mutation
