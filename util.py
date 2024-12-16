import itertools
from typing import Any, Iterable, Optional, Generic, Iterator

from type_defs import *


# Basic IO

def read_str(fname: str) -> str:
    with open(fname, 'r') as f:
        return f.read()


def lines(x: str) -> list[str]:
    return x.split('\n')


# Grid

def cgrid(x: str, fn=lambda x: x) -> Grid[str]:
    grid = []

    for row in lines(x):
        r = []
        for c in row:
            r.append(fn(c))
        grid.append(r)

    return grid


def dims(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0])


def in_grid(i: int, j: int, grid: Grid) -> bool:
    h, w = dims(grid)
    return 0 <= i < h and 0 <= j < w


def dir_dxy(dir: int) -> tuple[int, int]:
    if dir == 0:
        return 0, -1
    elif dir == 1:
        return 1, 0
    elif dir == 2:
        return 0, 1
    else:
        return -1, 0


def nbors(i: int, j: int, grid: Grid) -> list[tuple[int, int, int]]:
    res = []
    for d in range(0, 4):
        dx, dy = dir_dxy(d)
        if in_grid(i + dy, j + dx, grid):
            res.append((i + dy, j + dx, d))
    return res


def grid_iter(grid: Grid[T]) -> Iterable[tuple[int, int]]:
    h, w = dims(grid)
    return itertools.product(range(0, h), range(0, w))


# Union Find

class UF:
    def __init__(self, elems: Iterable[Any]):
        self.uf = {x: x for x in elems}
        self.groups = {x: {x} for x in elems}

    def find(self, x):
        if self.uf[x] == x:
            return x

        res = self.find(self.uf[x])
        self.uf[x] = res
        return res

    def union(self, x, y):
        cx, cy = self.find(x), self.find(y)
        if cx == cy:
            return
        gx, gy = self.groups[cx], self.groups[cy]

        if len(gx) > len(gy):
            cx, cy = cy, cx
            gx, gy = gy, gx

        self.uf[cx] = cy
        gy.update(gx)
        del self.groups[cx]

    def equiv(self, x, y) -> bool:
        return self.find(x) == self.find(y)

    def parts(self) -> dict[Any, set]:
        return self.groups


# Trees, BST

class TreeNode(Generic[T], Iterable[T]):
    def __init__(self, x: T):
        self.x = x
        self.l: Tree[T] = None
        self.r: Tree[T] = None

    def __len__(self):
        s = 1
        if self.l is not None:
            s += len(self.l)
        if self.r is not None:
            s += len(self.r)

        return s

    @staticmethod
    def in_order(t: "Tree[T]") -> Iterator[T]:
        if t is None:
            return

        yield from TreeNode.in_order(t.l)
        yield t.x
        yield from TreeNode.in_order(t.r)

    def __iter__(self) -> Iterator[T]:
        return TreeNode.in_order(self)


Tree: TypeAlias = Optional[TreeNode[T]]


# AVL Tree

class AvlNode:
    def __init__(self, x: Cmp):
        self.x = x
        self.h = 1


AvlTree: TypeAlias = Tree[AvlNode]


class BST(Iterable[Cmp]):
    def __init__(self, elems: Optional[Iterable[Cmp]] = None):
        self.root: Tree[AvlNode] = None

        if elems is not None:
            for x in elems:
                self.add(x)

    @staticmethod
    def find(t: AvlTree, x: Cmp) -> Optional[TreeNode[AvlNode]]:
        if t is None:
            return None

        if x == t.x.x:
            return t

        if x < t.x.x:
            return BST.find(t.l, x)
        else:
            return BST.find(t.r, x)

    @staticmethod
    def rotl(t: TreeNode[AvlNode]) -> TreeNode[AvlNode]:
        assert t.r is not None
        r = t.r
        t.r = r.l
        r.l = BST.rebalance(t)
        return r

    @staticmethod
    def rotr(t: TreeNode[AvlNode]) -> TreeNode[AvlNode]:
        assert t.l is not None
        l = t.l
        t.l = l.r
        l.r = BST.rebalance(t)
        return l

    @staticmethod
    def rebalance(t: TreeNode["AvlNode"]) -> TreeNode["AvlNode"]:
        lh = 0 if t.l is None else t.l.x.h
        rh = 0 if t.r is None else t.r.x.h
        t.x.h = 1 + max(lh, rh)
        root = t

        assert -2 <= lh-rh <= 2

        if lh >= rh + 2:
            assert root.l is not None
            llh = 0 if root.l.l is None else root.l.l.x.h
            lrh = 0 if root.l.r is None else root.l.r.x.h

            if llh >= lrh:
                root = BST.rotr(root)
            else:
                root.l = BST.rotl(root.l)
                root = BST.rotr(root)

            root = BST.rebalance(root)

        elif rh >= lh + 2:
            assert root.r is not None
            rlh = 0 if root.r.l is None else root.r.l.x.h
            rrh = 0 if root.r.r is None else root.r.r.x.h

            if rrh >= rlh:
                root = BST.rotl(root)
            else:
                root.r = BST.rotr(root.r)
                root = BST.rotl(root)

            root = BST.rebalance(root)

        return root

    @staticmethod
    def ins(t: AvlTree, x: Cmp) -> TreeNode[AvlNode]:
        if t is None:
            return TreeNode(AvlNode(x))

        if x == t.x.x:
            return t

        if x < t.x.x:
            t.l = BST.ins(t.l, x)
        else:
            t.r = BST.ins(t.r, x)

        return BST.rebalance(t)

    @staticmethod
    def rm_min(t: TreeNode[AvlNode]) -> tuple[AvlTree, Cmp]:
        if t.l is None:
            return t.r, t.x.x
        t.l, x = BST.rm_min(t.l)
        return BST.rebalance(t), x

    @staticmethod
    def rm_max(t: TreeNode[AvlNode]) -> tuple[AvlTree, Cmp]:
        if t.r is None:
            return t.r, t.x.x
        t.r, x = BST.rm_max(t.r)
        t = BST.rebalance(t)
        return t, x

    @staticmethod
    def rm_root(t: TreeNode[AvlNode]) -> AvlTree:
        if t.l is None:
            return t.r
        if t.r is None or t.l.x.h > t.r.x.h:
            t.l, t.x.x = BST.rm_max(t.l)
        else:
            t.r, t.x.x = BST.rm_min(t.r)
        return BST.rebalance(t)

    @staticmethod
    def rm(t: AvlTree, x: Cmp) -> AvlTree:
        if t is None:
            return t

        if x == t.x.x:
            return BST.rm_root(t)
        elif x < t.x.x:
            t.l = BST.rm(t.l, x)
        else:
            t.r = BST.rm(t.r, x)

        return BST.rebalance(t)

    @staticmethod
    def seg(t: AvlTree, lo: Cmp, hi: Cmp) -> Iterator[Cmp]:
        if t is None:
            return

        if lo < t.x.x:
            yield from BST.seg(t.l, lo, hi)
        if lo <= t.x.x < hi:
            yield t.x.x
        if t.x.x < hi:
            yield from BST.seg(t.r, lo, hi)

    def add(self, x: Cmp):
        self.root = BST.ins(self.root, x)

    def remove(self, x: Cmp):
        self.root = BST.rm(self.root, x)

    def pred(self, x: Cmp) -> Optional[Cmp]:
        if self.root is None:
            return None

        p = None
        cur = self.root

        while cur.x.x != x:
            if x < cur.x.x:
                cur = cur.l
            else:
                p = cur
                cur = cur.r

            if cur is None:
                return None

        if cur.l is None:
            return None if p is None else p.x.x

        cur = cur.l

        while cur.r is not None:
            cur = cur.r

        return cur.x.x

    def succ(self, x: Cmp) -> Optional[Cmp]:
        if self.root is None:
            return None

        p = None
        cur = self.root

        while cur.x.x != x:
            if x < cur.x.x:
                p = cur
                cur = cur.l
            else:
                cur = cur.r

            if cur is None:
                return None

        if cur.r is None:
            return None if p is None else p.x.x

        cur = cur.r

        while cur.l is not None:
            cur = cur.l

        return cur.x.x

    def min(self) -> Optional[Cmp]:
        t = self.root
        if t is None:
            return None
        while t.l is not None:
            t = t.l
        return t.x.x

    def max(self) -> Optional[Cmp]:
        t = self.root
        if t is None:
            return None
        while t.r is not None:
            t = t.r
        return t.x.x

    def range(self, lo: Cmp, hi: Cmp) -> Iterator[Cmp]:
        return BST.seg(self.root, lo, hi)

    def __contains__(self, item: Cmp) -> bool:
        return BST.find(self.root, item) is not None

    def __iter__(self) -> Iterator[Cmp]:
        return map(lambda t: t.x, self.root)

    def __len__(self) -> int:
        return len(self.root)
