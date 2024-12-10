from util import *


def tdfs(tmap, visited, i, j, n, paths=None, cur_path=None):
    if paths is None:
        paths = set()
        cur_path = ((i, j),)

    if tmap[i][j] != n:
        return 0

    if visited is not None and (i, j) in visited:
        return 0

    if visited is None and (cur_path + ((i, j),)) in paths:
        return 0

    if visited is not None:
        visited.add((i, j))

    if tmap[i][j] == 9:
        paths.add(cur_path + ((i, j),))
        return 1

    res = 0

    for p, q in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
        if not (0 <= p < len(tmap) and 0 <= q < len(tmap[0])):
            continue

        res += tdfs(tmap, visited, p, q, n+1, paths, cur_path + ((i,j),))

    return res


def part1(x):
    tmap = cgrid(x, int)

    res = 0

    for i in range(0, len(tmap)):
        for j in range(0, len(tmap[0])):
            visited = set()
            res += tdfs(tmap, visited, i, j, 0)

    return res



def part2(x):
    tmap = cgrid(x, int)

    paths = set()

    for i in range(0, len(tmap)):
        for j in range(0, len(tmap[0])):
            tdfs(tmap, None, i, j, 0, paths, ((i, j),))

    return len(paths)


if __name__ == "__main__":
    part1_test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 36
    assert part2(part2_test) == 81

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
