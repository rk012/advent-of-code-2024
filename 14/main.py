import re
import sys

from util import *


def parse(x):
    res = []
    for s in lines(x):
        px, py, vx, vy = map(int, re.findall(r"-?\d+", s))
        res.append([px, py, vx, vy])
    return res


def part1(x, W=101, H=103):
    bots = parse(x)

    for _ in range(0, 100):
        for r in bots:
            r[0] += r[2]
            r[1] += r[3]
            r[0] %= W
            r[1] %= H

            assert 0 <= r[0] < W
            assert 0 <= r[1] < H

    q1, q2, q3, q4 = 0,0,0,0

    mw = (W-1) // 2
    mh = (H-1) // 2
    for px, py, _, _ in bots:
        if px < mw and py < mh:
            q1 += 1
        elif px < mw and py > mh:
            q2 += 1
        elif px > mw and py < mh:
            q3 += 1
        elif px > mw and py > mh:
            q4 += 1

    return q1*q2*q3*q4


def part2(x, W=101, H=103):
    bots = parse(x)

    i = 0

    while True:
        for r in bots:
            r[0] += r[2]
            r[1] += r[3]
            r[0] %= W
            r[1] %= H

            assert 0 <= r[0] < W
            assert 0 <= r[1] < H

        i += 1

        visited = set()
        flag = True

        for px, py, _, _ in bots:
            if (px, py) in visited:
                flag = False
                break

            visited.add((px, py))

        if flag:
            grid = [['.' for _ in range(0, W)] for _ in range(0, H)]

            for px, py in visited:
                grid[py][px] = 'X'

            print("\n\n")
            for row in grid:
                print(''.join(row))

            return i


if __name__ == "__main__":
    part1_test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test, 11, 7))
    # print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test, 11, 7) == 12
    # assert part2(part2_test)

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
