from heapq import heappush as hpush, heappop as hpop

from util import *


def part1(x):
    grid = cgrid(x)

    x0, y0 = 0, 0

    for i, j in grid_iter(grid):
        if grid[i][j] == 'S':
            x0, y0 = j, i

    q = []
    visited = set()
    hpush(q, (0, x0, y0, 1))

    while q:
        s, x, y, d = hpop(q)
        if (x, y, d) in visited:
            continue
        visited.add((x, y, d))

        if not in_grid(y, x, grid):
            continue
        if grid[y][x] == '#':
            continue
        elif grid[y][x] == 'E':
            return s

        dx, dy = dir_dxy(d)

        hpush(q, (s+1, x+dx, y+dy, d))
        hpush(q, (s+1000, x, y, (d+1)%4))
        hpush(q, (s+1000, x, y, (d-1)%4))


def part2(x):
    grid = cgrid(x)

    x0, y0 = 0, 0

    for i, j in grid_iter(grid):
        if grid[i][j] == 'S':
            x0, y0 = j, i

    q = []
    visited = dict()
    hpush(q, (0, x0, y0, 1, {(x0, y0)}))

    pos = set()
    mins = None

    while q:
        s, x, y, d, path = hpop(q)

        if (x, y, d) in visited:
            if visited[(x, y, d)] < s:
                continue
        visited[(x, y, d)] = s

        if not in_grid(y, x, grid):
            continue
        if grid[y][x] == '#':
            continue
        elif grid[y][x] == 'E':
            if mins is None:
                mins = s
                pos = path.copy()
                continue
            else:
                if s > mins:
                    continue
                pos.update(path)

        dx, dy = dir_dxy(d)

        p0, p1, p2 = path.copy(), path.copy(), path.copy()
        p2.add((x+dx, y+dy))
        p0.add((x, y))
        p1.add((x, y))

        hpush(q, (s+1, x+dx, y+dy, d, p2))
        hpush(q, (s+1000, x, y, (d+1)%4, p0))
        hpush(q, (s+1000, x, y, (d-1)%4, p1))

    return len(pos)


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

    assert part1(part1_test) == 7036

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test)
    print("Part 2 (test):", part2(part2_test))

    assert part2(part2_test) == 45

    print("Part 2:", part2(test_file))
