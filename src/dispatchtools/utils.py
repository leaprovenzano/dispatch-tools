from typing import Callable
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
