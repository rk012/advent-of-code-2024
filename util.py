import itertools
import re
from collections import deque, defaultdict
from heapq import heappush, heappop
from typing import Any, Iterator, Callable

from type_defs import *


# Basic IO

def read_str(fname: str) -> str:
    with open(fname, 'r') as f:
        return f.read()


def lines(x: str) -> list[str]:
    return x.split('\n')


def read_ints(s: str) -> Iterable[int]:
    return map(int, re.findall(r"-?\d+", s))


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


# Graphs

class Graph(ImplGraph[T]):
    def __init__(self, v: Optional[Iterable[T]] = None, directed=False):
        self._dir = directed
        self._nbors: dict[T, set[tuple[T, Cmp]]] = dict()
        self.edges: dict[tuple[T, T], Cmp] = dict()

        if v is not None:
            for x in v:
                self.add_vert(x)

    @property
    def directed(self) -> bool:
        return self._dir

    def nbors(self, v: T) -> Iterable[tuple[T, Cmp]]:
        return self._nbors[v]

    @property
    def vertices(self) -> Iterable[T]:
        return self._nbors.keys()

    def add_vert(self, v: T):
        if v not in self._nbors:
            self._nbors[v] = set()

    def add_edge(self, u: T, v: T, w: Cmp = 1):
        assert u in self._nbors
        assert v in self._nbors
        self.edges[(u, v)] = w
        self._nbors[u].add((v, w))
        if not self.directed:
            self.edges[(v, u)] = w
            self._nbors[v].add((u, w))

    def del_edge(self, u: T, v: T):
        assert u in self._nbors
        assert v in self._nbors
        del self.edges[(u, v)]
        self._nbors[u] = set(filter(lambda x: x[0] != v, self._nbors[u]))
        if not self.directed:
            del self.edges[(v, u)]
            self._nbors[v] = set(filter(lambda x: x[0] != u, self._nbors[v]))

    def get_edge(self, u: T, v: T) -> Optional[Cmp]:
        return None if (u, v) not in self.edges else self.edges[(u, v)]

    def kruskals(self) -> "Graph[T]":
        assert not self.directed
        edges = []
        mst = Graph(self._nbors.keys())
        uf = UF(self._nbors.keys())

        for (u, v), w in self.edges.items():
            heappush(edges, (w, u, v))

        while edges:
            _, u, v = heappop(edges)
            if not uf.equiv(u, v):
                uf.union(u, v)
                mst.add_edge(u, v)

        return mst

    def components(self) -> Iterable[set[T]]:
        assert not self.directed
        uf = UF(self._nbors.keys())

        for u, v in self.edges.keys():
            uf.union(u, v)

        return uf.groups.values()


class Path(Iterable[T]):
    def __init__(self, x: T, base: Optional["Path[T]"] = None):
        self.base = base
        self.x = x

    def __add__(self, other: T) -> "Path[T]":
        return Path(other, self)

    def __iter__(self):
        q = deque()
        p = self
        while p is not None:
            q.appendleft(p.x)
            p = p.base
        return iter(q)


class KeyCmp(Cmp, Generic[T]):
    def __init__(self, k: Cmp, v: T):
        self.k = k
        self.v = v
        self.__eq__ = k.__eq__
        self.__lt__ = k.__lt__

    def __eq__(self, other):
        if not isinstance(other, KeyCmp):
            return NotImplemented
        return self.k == other.k

    def __lt__(self, other):
        if not isinstance(other, KeyCmp):
            return NotImplemented
        return self.k < other.k

    def __getitem__(self, i) -> Cmp | T:
        if i == 0:
            return self.k
        elif i == 1:
            return self.v
        else:
            raise IndexError()


class ShortestPath(Traversal[T, Optional[tuple[Path[T], float]], KeyCmp[tuple[Path[T], T]]]):
    def __init__(self, targets: Iterable[T], heuristic: Callable[[T], float] = lambda _: 0):
        super().__init__()
        self.targets = set(targets)
        self.visited = set()
        self.heuristic = heuristic

    def start(self, v: T) -> KeyCmp[tuple[Path[T], T]]:
        return KeyCmp((0, 0), (Path(v), v))

    def visit(self, ctx: KeyCmp[tuple[Path[T], T]]) -> bool:
        (c, _), (p, v) = ctx
        if v in self.targets:
            self.result = p, c
            return False
        if v in self.visited:
            return False
        self.visited.add(v)
        return True

    def nbor(self, cur: KeyCmp[tuple[Path[T], T]], nxt: T, w: float) -> Optional[KeyCmp[tuple[Path[T], T]]]:
        (c, h0), (p, v) = cur
        c -= h0
        c += w
        h = self.heuristic(nxt)
        return KeyCmp((c+h, h), (p+nxt, nxt))

    def end(self) -> Optional[Path[T]]:
        return None


def search(g: ImplGraph[T], t: Traversal[T, R, C], start: T, single_visit: bool = True, dfs: bool = False) -> R:
    q = deque([(start, t.start(start))])
    visited = set()

    while q:
        if t.result is not None:
            return t.result

        if dfs:
            cur, ctx = q.pop()
        else:
            cur, ctx = q.popleft()

        if single_visit and cur in visited:
            continue
        visited.add(cur)

        if not t.visit(ctx):
            continue

        for nxt, w in g.nbors(cur):
            new_ctx = t.nbor(ctx, nxt, w)
            if new_ctx is not None:
                q.append((nxt, new_ctx))

    return t.end()


def astar(g: ImplGraph[T], t: Traversal[T, R, C], start: T, single_visit: bool = True) -> R:
    pq = [KeyCmp(t.start(start), start)]
    visited = set()

    while pq:
        if t.result is not None:
            return t.result

        ctx, cur = heappop(pq)

        if single_visit and cur in visited:
            continue
        visited.add(cur)

        if not t.visit(ctx):
            continue

        for nxt, w in g.nbors(cur):
            new_ctx = t.nbor(ctx, nxt, w)
            if new_ctx is not None:
                heappush(pq, KeyCmp(new_ctx, nxt))

    return t.end()


def build_graph(g: ImplGraph[T], *roots: T):
    res = Graph(directed=g.directed)
    q = deque(roots)
    visited = set()

    while q:
        u = q.popleft()
        if u in visited:
            continue
        visited.add(u)
        res.add_vert(u)
        for v, w in g.nbors(u):
            q.append(v)
            res.add_vert(v)
            res.add_edge(u, v, w)

    return res


def topsort(g: Graph[T]) -> list[T]:
    assert g.directed
    counts = defaultdict(lambda: 0)
    verts = set(g.vertices)

    for v in verts:
        for u, _ in g.nbors(v):
            counts[u] += 1

    q = deque([v for v in verts if counts[v] == 0])
    res = []

    while q:
        v = q.popleft()
        res.append(v)

        for u, _ in g.nbors(v):
            counts[u] -= 1
            if counts[u] == 0:
                q.append(u)

    assert len(res) == len(verts)

    return res[::-1]


class GridGraph(ImplGraph):
    def __init__(self, grid):
        self.grid = grid

    @property
    def directed(self) -> bool:
        return False

    def nbors(self, v: T) -> Iterable[tuple[T, Cmp]]:
        i, j = v
        for d in range(0, 4):
            dx, dy = dir_dxy(d)
            if in_grid(i+dy, j+dx, self.grid):
                yield (i+dy, j+dx), 1
