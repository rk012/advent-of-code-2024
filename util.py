from typing import Any, Iterable, Optional, TypeAlias, TypeVar


def read_str(fname: str) -> str:
    with open(fname, 'r') as f:
        return f.read()


def lines(x: str) -> list[str]:
    return x.split('\n')


T = TypeVar("T")

Grid: TypeAlias = list[list[T]]


def cgrid(x: str, fn=lambda x: x) -> Grid[str]:
    grid = []

    for row in lines(x):
        r = []
        for c in row:
            r.append(fn(c))
        grid.append(r)

    return grid


# Grid

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

