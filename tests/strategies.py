# flake8: noqa : F405
import typing

from hypothesis.strategies import *  # noqa: F403


def _hack_from_type(t):
    """this hack patches a bug in hypothesis.strategies.from_type for typing.Hashable and typing.Sized.

    see issue at https://github.com/HypothesisWorks/hypothesis/issues/2272
    """
    print('hack called')
    if t in (typing.Hashable, typing.Sized):
        return from_type(t.__origin__)
    return from_type(t)


register_type_strategy(typing.Hashable, _hack_from_type(typing.Hashable))
register_type_strategy(typing.Sized, _hack_from_type(typing.Sized))


def everything_except(*excluded_types):
    return from_type(type).flatmap(from_type).filter(lambda x: not isinstance(x, excluded_types))
