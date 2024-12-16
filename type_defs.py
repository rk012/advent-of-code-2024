from typing import TypeVar, TypeAlias, Protocol

T = TypeVar("T")

Grid: TypeAlias = list[list[T]]


class PartialOrd(Protocol):
    def __le__(self, other):
        pass


class Cmp(Protocol):
    def __lt__(self, other):
        pass

    def __eq__(self, other):
        pass
