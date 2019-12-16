import typing
from typing import Callable, Any
import inspect


def accepts_args(f: Callable) -> bool:
    """return true if the callable f has args other than self.

    Note:
       here the an method that is self only is determined only by the `self` name
       so if you've decided to name the `self` parameter something silly. it will
       not work.... we will look for a less fragile way to handle this in future.
    """
    params = inspect.signature(f).parameters
    return len(params) > 0 and list(params) != ['self']


def is_type(t: Any) -> bool:
    """return true if t is a type

    Example:
        >>> from typing import List, Hashable
        >>> from dispatchtools.utils import is_type
        >>>
        >>> is_type(int)
        True
        >>> is_type(10)
        False
    """
    return isinstance(t, type)


def is_generic(t: type) -> bool:
    """return True if `t` is a generic type from typing.

    Example:
        >>> from typing import List, Hashable
        >>> from dispatchtools.utils import is_generic
        >>>
        >>> is_generic(int)
        False
        >>> is_generic(List[str])
        True
        >>> is_generic(Hashable)
        True
    """
    return isinstance(t, typing._GenericAlias)  # type: ignore
