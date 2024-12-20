from util import *


class GGraph(GridGraph):
    def nbors(self, v: T) -> Iterable[tuple[T, Cmp]]:
        for (i, j), _ in super().nbors(v):
            if self.grid[i][j] != '#':
                yield (i, j), 1


class EndDist(Traversal):
    def __init__(self, costs, target):
        super().__init__()
        self.costs = costs
        self.paths = []
        self.target = target
        self.visited = set()

    def start(self, v: T) -> KeyCmp[tuple[Path[T], T]]:
        return KeyCmp((0, 0), (Path(v), v))

    def visit(self, ctx: KeyCmp[tuple[Path[T], T]]) -> bool:
        (c, _), (p, v) = ctx

        if v == self.target:
            self.paths.append(p)

        if v in self.visited:
            return False
        self.visited.add(v)
        self.costs[v[0]][v[1]] = c
        return True

    def nbor(self, cur: KeyCmp[tuple[Path[T], T]], nxt: T, w: float) -> Optional[KeyCmp[tuple[Path[T], T]]]:
        (c, h0), (p, v) = cur
        c -= h0
        c += w
        h = 0
        return KeyCmp((c+h, h), (p+nxt, nxt))

    def end(self) -> Optional[Path[T]]:
        return self.paths


def part1(x, lim=100):
    grid = cgrid(x)
    h, w = dims(grid)
    costs = [[None for _ in range(0, w)] for _ in range(0, h)]
    gr = GGraph(grid)

    i0, j0 = 0, 0
    i1, j1 = 1, 1

    for i, j in grid_iter(grid):
        c = grid[i][j]
        if c == 'S':
            i0, j0 = i, j
        elif c == 'E':
            i1, j1 = i, j

    paths = search(gr, EndDist(costs, (i0, j0)), (i1, j1))

    chts = set()

    for p in paths:
        for i, j in p:
            for u, v, d in nbors(i, j, costs):
                dx, dy = dir_dxy(d)
                u1, v1 = u+dy, v+dx
                if not in_grid(u1, v1, costs):
                    continue
                c1 = costs[u1][v1]
                if c1 is None:
                    continue
                c0 = costs[i][j]
                dc = c1 - c0
                if dc+2 <= -lim:
                    chts.add((u, v))

    return len(chts)


def part2(x, lim=100):
    grid = cgrid(x)
    h, w = dims(grid)
    costs = [[None for _ in range(0, w)] for _ in range(0, h)]
    gr = GGraph(grid)

    i0, j0 = 0, 0
    i1, j1 = 1, 1

    for i, j in grid_iter(grid):
        c = grid[i][j]
        if c == 'S':
            i0, j0 = i, j
        elif c == 'E':
            i1, j1 = i, j

    paths = search(gr, EndDist(costs, (i0, j0)), (i1, j1))
    assert len(paths) == 1
    p = paths[0]
    chts = set()

    for i, j in p:
        c0 = costs[i][j]
        for i1 in range(i-20, i+20+1):
            di = abs(i-i1)
            for j1 in range(j-(20-di), j+(20-di)+1):
                td = di + abs(j1 - j)
                assert td <= 20

                if not in_grid(i1, j1, costs) or costs[i1][j1] is None:
                    continue

                c1 = costs[i1][j1]
                dc = c1 - c0
                if dc+td <= -lim:
                    chts.add((i, j, i1, j1))

    return len(chts)


if __name__ == "__main__":
    part1_test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test, 36)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 4

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test, 67)
    print("Part 2 (test):", p2_tst)

    assert p2_tst == 55

    print("Part 2:", part2(test_file))
