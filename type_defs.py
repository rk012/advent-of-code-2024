from abc import ABC, abstractmethod
from typing import TypeVar, TypeAlias, Protocol, Iterable, Generic, Optional

T = TypeVar("T")
R = TypeVar("R")
C = TypeVar("C")

Grid: TypeAlias = list[list[T]]


class PartialOrd(Protocol):
    def __le__(self, other):
        pass


class Cmp(Protocol):
    def __lt__(self, other):
        pass

    def __eq__(self, other):
        pass


class ImplGraph(ABC, Generic[T]):
    @property
    @abstractmethod
    def directed(self) -> bool:
        pass

    @abstractmethod
    def nbors(self, v: T) -> Iterable[tuple[T, Cmp]]:
        pass


class Traversal(ABC, Generic[T, R, C]):
    def __init__(self):
        self.result: Optional[R] = None

    @abstractmethod
    def start(self, v: T) -> C:
        pass

    @abstractmethod
    def visit(self, ctx: C) -> bool:
        pass

    @abstractmethod
    def nbor(self, cur: C, nxt: T, w: Cmp) -> Optional[C]:
        pass

    @abstractmethod
    def end(self) -> R:
        pass
