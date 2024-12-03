from util import *

import re


def part1(x):
    res = 0

    for m in re.findall(r"mul\(\d+,\d+\)", x):
        a, b = map(int, re.findall(r"\d+", m))
        res += a*b

    return res


def part2(x):
    res = 0
    active = True

    for m in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", x):
        if m[0:3] == "don":
            active = False
            continue

        if m[0:2] == "do":
            active = True
            continue

        if not active:
            continue

        a, b = map(int, re.findall(r"\d+", m))
        res += a*b

    return res


if __name__ == "__main__":
    part1_test = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

    part2_test = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 161
    assert part2(part2_test) == 48

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
