from util import *


def parse_lines(lines):
    n1, n2 = [], []

    for line in lines:
        n1.append(int(line.split("   ")[0]))
        n2.append(int(line.split("   ")[1]))

    return n1, n2


def part1(x):
    n1, n2 = parse_lines(x.split("\n"))
    res = 0

    for (x, y) in zip(sorted(n1), sorted(n2)):
        res += abs(x-y)

    return res


def part2(x):
    n1, n2 = parse_lines(x.split("\n"))
    res = 0

    for x in n1:
        i = 0

        for y in n2:
            if x == y:
                i += 1

        res += x*i

    return res


if __name__ == "__main__":
    part1_test = """3   4
4   3
2   5
1   3
3   9
3   3"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    assert part1(part1_test) == 11
    assert part2(part2_test) == 31

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
