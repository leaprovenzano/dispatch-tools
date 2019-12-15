from typing import Optional, Callable


class InvalidCallableError(TypeError):

    _base_msg = 'callable{} is invalid as a dispatch function.{}'

    def __init__(self, callable: Optional[Callable] = None, reason: Optional[str] = None):
        f = f' : {callable}' if callable else ''
        r = f' {reason}' if reason else ''
        self.msg = self._base_msg.format(f, r)

    def __str__(self):
        return self.msg
