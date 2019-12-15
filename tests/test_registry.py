from typing import Hashable, Callable


import pytest


from hypothesis import given, infer, assume


from dispatchtools.registry import Registry


from tests import strategies as st
from tests.utils import dependency


class TestRegistry:

    registry = None

    @dependency
    def test_init_registry(self):
        self.__class__.registry = Registry()
        pass

    @dependency(depends=['init_registry'])
    def test_missing(self):
        with pytest.raises(KeyError):
            self.registry['missing']

    @given(key=infer, value=st.everything_except(Callable))
    @dependency(depends=['init_registry'])
    def test_register_invalid_values(self, key: Hashable, value):
        assume(key not in self.registry)
        with pytest.raises(TypeError, match='Registry values must be callable'):
            self.registry.register(key, value)
        assert key not in self.registry

    @given(key=infer, value=infer)
    @dependency(depends=['init_registry'])
    def test_register(self, key: Hashable, value: Callable):
        assume(key not in self.registry)
        self.registry.register(key, value)
        assert self.registry[key] == value

    @dependency(depends=['register'])
    def test_pop_fails(self):
        with pytest.raises(TypeError):
            self.registry.pop()

    @dependency(depends=['register'])
    def test_update_fails(self):
        with pytest.raises(TypeError):
            self.registry.update(a=lambda x: x, b=lambda x: x)

    @given(key=infer, value=infer)
    @dependency(depends=['register'])
    def test_setitem_fails(self, key: Hashable, value: Callable):
        assume(key not in self.registry)
        with pytest.raises(TypeError):
            self.registry[key] = value

    @dependency(depends=['register'])
    def test_cannot_register_existing_key(self):
        key = list(self.registry)[-1]
        with pytest.raises(TypeError):
            self.registry.register(key, lambda x: x)
