import re
from heapq import heappush as hpush, heappop as hpop

from util import *


def parse(x):
    res = []
    for s in x.split("\n\n"):
        al, bl, pl = lines(s)
        ax, ay = map(int, re.findall(r"\d+", al))
        bx, by = map(int, re.findall(r"\d+", bl))
        px, py = map(int, re.findall(r"\d+", pl))

        res.append(((ax, ay), (bx, by), (px, py)))
    return res


def part1(x):
    blocks = parse(x)
    res = 0

    for (ax, ay), (bx, by), (px, py) in blocks:
        pq = []
        visited = set()
        hpush(pq, (0, 0, 0, 0, 0))

        while pq:
            cost, x, y, a, b = hpop(pq)

            if (x, y) in visited:
                continue

            visited.add((x, y))

            if (x, y) == (px, py):
                res += cost
                break

            if a < 100:
                hpush(pq, (cost+3, x+ax, y+ay, a+1, b))

            if b < 100:
                hpush(pq, (cost+1, x+bx, y+by, a, b+1))

    return res


def part2(x, off=10000000000000):
    blocks = parse(x)
    res = 0

    for (ax, ay), (bx, by), (px, py) in blocks:
        px += off
        py += off

        det = ax*by - bx*ay

        assert det != 0

        a, b, c, d = by/det, -bx/det, -ay/det, ax/det

        A = round(a*px+b*py)
        B = round(c*px+d*py)

        if ax*A+bx*B == px and ay*A+by*B == py:
            res += 3*A + B

    return res


if __name__ == "__main__":
    part1_test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 480
    assert part2(part2_test, 0) == 480

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
