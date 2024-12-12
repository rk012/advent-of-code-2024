from util import *


def pdfs(grid, c, i, j, group):
    if not (0 <= i < len(grid)):
        return

    if not (0 <= j < len(grid[0])):
        return

    if grid[i][j] != c:
        return

    if (i, j) in group:
        return

    group.add((i, j))

    pdfs(grid, c, i-1, j, group)
    pdfs(grid, c, i+1, j, group)
    pdfs(grid, c, i, j+1, group)
    pdfs(grid, c, i, j-1, group)


def dir_dxy(dir):
    if dir == 0:
        return 0, -1
    elif dir == 1:
        return 1, 0
    elif dir == 2:
        return 0, 1
    else:
        return -1, 0


def part1(x):
    grid = cgrid(x)

    mark = set()

    acc = 0

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (i, j) not in mark:
                group = set()
                c = grid[i][j]
                pdfs(grid, c, i, j, group)

                a = len(group)
                pr = 0

                for (p,q) in group:
                    cds = [(p-1,q), (p+1,q), (p,q-1), (p,q+1)]

                    for (h,k) in cds:
                        if not (0 <= h < len(grid)):
                            pr += 1
                            continue
                        if not (0 <= k < len(grid[0])):
                            pr += 1
                            continue
                        if grid[h][k] != c:
                            pr += 1

                acc += a*pr
                mark.update(group)

    return acc


def part2(x):
    grid = cgrid(x)

    mark = set()

    acc = 0

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (i, j) not in mark:
                group = set()
                c = grid[i][j]
                pdfs(grid, c, i, j, group)

                a = len(group)

                segs = set()

                for (p,q) in group:
                    cds = [(p-1,q, 0), (p+1,q, 2), (p,q-1, 3), (p,q+1, 4)]

                    for (h,k,d) in cds:
                        if not (0 <= h < len(grid)):
                            segs.add((h,k,d))
                            continue
                        if not (0 <= k < len(grid[0])):
                            segs.add((h,k,d))
                            continue
                        if grid[h][k] != c:
                            segs.add((h,k,d))

                flag = True
                while flag:
                    flag = False
                    ns = segs.copy()

                    for (p,q,d) in segs:
                        dp, dq = dir_dxy(d)

                        # +
                        q1 = q+dq
                        p1 = p+dp

                        while (p1, q1, d) in segs:
                            ns.remove((p1, q1, d))
                            p1 += dp
                            q1 += dq

                        # -
                        q1 = q-dq
                        p1 = p-dp

                        while (p1, q1, d) in segs:
                            ns.remove((p1, q1, d))
                            p1 -= dp
                            q1 -= dq

                        if segs != ns:
                            flag = True
                            break

                    if flag:
                        segs = ns

                pr = len(segs)
                acc += a*pr


                mark.update(group)

    return acc


if __name__ == "__main__":
    part1_test = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 1930
    assert part2(part2_test) == 1206

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
