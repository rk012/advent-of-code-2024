from util import *


# I really should add something like this to utils
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
            if in_grid(i+dy, j+dx, self.grid) and self.grid[i+dy][j+dx]:
                yield (i+dy, j+dx), 1


def part1(x, w=71, m=1024):
    grid = [[True for _ in range(0, w)] for _ in range(0, w)]
    g = GridGraph(grid)

    edg = []

    for line in lines(x):
        edg.append(tuple(read_ints(line)))

    for n, (i, j) in enumerate(edg):
        if n == m:
            break
        grid[i][j] = False

    return search(g, ShortestPath([(w-1, w-1)]), (0, 0))[1]


def part2(x, w=71):
    grid = [[True for _ in range(0, w)] for _ in range(0, w)]
    g = GridGraph(grid)

    edg = deque()

    for line in lines(x):
        edg.append(tuple(read_ints(line)))

    res = search(g, ShortestPath([(w-1, w-1)]), (0, 0))
    last = None

    while res is not None:
        p = res[0]
        nodes = set(p)

        while edg:
            i, j = edg.popleft()
            grid[i][j] = False
            if (i, j) in nodes:
                last = (i, j)
                break

        res = search(g, ShortestPath([(w-1, w-1)]), (0, 0))

    return ','.join(map(str, last))


if __name__ == "__main__":
    part1_test = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test, 7, 12)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 22

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test, 7)
    print("Part 2 (test):", p2_tst)

    assert p2_tst == "6,1"

    print("Part 2:", part2(test_file))
