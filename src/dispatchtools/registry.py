from typing import Hashable, Callable


class Registry(dict):

    """A Registry is a mostly immutable mapping of hashable to callables.

    Entries may only be created using the `register` method and may not be further modified after creation.
    """

    def register(self, key: Hashable, value: Callable = None) -> Callable:
        if key in self:
            self._on_mutation()
        if not callable(value):
            raise TypeError(f'{self.__class__.__name__} values must be callable')
        super().__setitem__(key, value)

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
