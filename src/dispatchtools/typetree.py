from typing import Tuple, List


class Sentry:

    __inst__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__inst__ is None:
            cls.__inst__ = super().__new__(cls)
        return cls.__inst__


SENTRY = Sentry()


def isroot(t: type) -> bool:
    return t is object


class TypeTree(dict):

    def __init__(self):
        super().__init__({object: None})

    def add(self, typ: type):
        if typ in self or not typ.__bases__:
            return
        parents = typ.__bases__
        self[typ] = parents[0] if len(parents) == 1 else SENTRY
        for parent in parents:
            self.add(parent)

    def depth(self, node: type, _pos: int = 0) -> int:
        if isroot(node):
            return _pos
        parent = self[node]
        if parent is SENTRY:
            return 1
        return self.depth(parent, _pos + 1)

    def get_children(self, t: type) -> List[type]:
        return [k for k, v in self.items() if v == t]

    def _nearest_parent(self, t: type, _distance: int = 0):
        if isroot(t):
            raise KeyError('roots have no parents')
        if t in self:
            return t, _distance

        if len(t.__bases__) > 1:
            raise KeyError(
                'cant find parent for unregistered type with multiple parents' 'try registering your class directly'
            )

        parent = t.__bases__[0]
        return self._nearest_parent(parent, _distance=_distance + 1)

    def nearest_parent(self, t: type) -> type:
        parent, _ = self._nearest_parent(t)
        return parent

    def nearest_parent_with_distance(self, t: type) -> Tuple[type, int]:
        return self._nearest_parent(t)
