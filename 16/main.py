from util import *


class GridGraph(ImplGraph):
    def __init__(self, grid):
        self.grid = grid

    @property
    def directed(self) -> bool:
        return False

    def nbors(self, v: T) -> Iterable[tuple[T, Cmp]]:
        i, j, d = v
        dx, dy = dir_dxy(d)
        if in_grid(i+dy, j+dx, self.grid) and self.grid[i+dy][j+dx] != '#':
            yield (i+dy, j+dx, d), 1
        yield (i, j, (d+1)%4), 1000
        yield (i, j, (d-1)%4), 1000


def part1(x):
    grid = cgrid(x)

    x0, y0 = 0, 0
    x1, y1 = 0, 0

    for i, j in grid_iter(grid):
        if grid[i][j] == 'S':
            x0, y0 = j, i
        elif grid[i][j] == 'E':
            x1, y1 = j, i

    targets = [(y1, x1, d) for d in range(0, 4)]

    _, c = astar(GridGraph(grid), ShortestPath(targets), (y0, x0, 1))
    return c


class GridPath(ShortestPath):
    def __init__(self, targets: Iterable[T]):
        def h(v):
            i, j, d = v
            i1, j1, _ = list(targets)[0]

            if i == i1 and j == j1:
                return 0

            dx1, dy1 = dir_dxy(d)
            dot = dx1*(j1-j) + dy1*(i1-i)
            c = abs(i-i1) + abs(j-j1)
            if dot <= 0:
                c += 1000
            if i != i1 and j != j1:
                c += 1000

            return c

        super().__init__(targets, h)
        self.cost = None
        self.paths = []
        self.min_costs = {}

    def visit(self, ctx: KeyCmp[tuple[Path[T], T]]) -> bool:
        (c, _), (p, v) = ctx

        if v in self.min_costs and self.min_costs[v] < c:
            return False
        self.min_costs[v] = c

        if self.cost is not None and c > self.cost:
            verts = set()
            for p in self.paths:
                for i, j, _ in p:
                    verts.add((i, j))

            self.result = len(verts)
            return False

        if v in self.targets:
            self.cost = c
            self.paths.append(p)

        return True


def part2(x):
    grid = cgrid(x)

    x0, y0 = 0, 0
    x1, y1 = 0, 0

    for i, j in grid_iter(grid):
        if grid[i][j] == 'S':
            x0, y0 = j, i
        elif grid[i][j] == 'E':
            x1, y1 = j, i

    targets = [(y1, x1, d) for d in range(0, 4)]

    r = astar(GridGraph(grid), GridPath(targets), (y0, x0, 1), False)
    return r


if __name__ == "__main__":
    part1_test = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 7036

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test)
    print("Part 2 (test):", p2_tst)

    assert p2_tst == 45

    print("Part 2:", part2(test_file))
