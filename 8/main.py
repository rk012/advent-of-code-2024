from collections import defaultdict

from util import *


def part1(x):
    agrid = cgrid(x)
    locs = defaultdict(lambda: [])
    res = set()

    h = len(agrid)
    w = len(agrid[0])

    for i in range(0, h):
        for j in range(0, w):
            if agrid[i][j] != '.':
                locs[agrid[i][j]].append((i, j))

    for a in locs.keys():
        for (i1, j1) in locs[a]:
            for (i2, j2) in locs[a]:
                if i1 == i2 and j1 == j2:
                    continue

                ip1, ip2 = 2*i1-i2, 2*i2-i1
                jp1, jp2 = 2*j1-j2, 2*j2-j1

                if 0 <= ip1 < h and 0 <= jp1 < w:
                    res.add((ip1, jp1))

                if 0 <= ip2 < h and 0 <= jp2 < w:
                    res.add((ip2, jp2))

    return len(res)





def part2(x):
    agrid = cgrid(x)
    locs = defaultdict(lambda: [])
    res = set()

    h = len(agrid)
    w = len(agrid[0])

    for i in range(0, h):
        for j in range(0, w):
            if agrid[i][j] != '.':
                locs[agrid[i][j]].append((i, j))

    for a in locs.keys():
        for (i1, j1) in locs[a]:
            for (i2, j2) in locs[a]:
                if i1 == i2 and j1 == j2:
                    continue

                n = 0
                while True:
                    p, q = i2+n*(i2-i1), j2+n*(j2-j1)
                    if not (0 <= p < h and 0 <= q < w):
                        break

                    res.add((p, q))
                    n += 1

                n = 0
                while True:
                    p, q = i1+n*(i1-i2), j1+n*(j1-j2)
                    if not (0 <= p < h and 0 <= q < w):
                        break

                    res.add((p, q))
                    n += 1

    return len(res)


if __name__ == "__main__":
    part1_test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 14
    assert part2(part2_test) == 34

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
