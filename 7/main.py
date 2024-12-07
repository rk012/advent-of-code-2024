from util import *


def parse_line(x):
    a, b = x.split(': ')
    return int(a), list(map(int, b.split(' ')))


def try_solve(nums, target, concat=False):
    if target < 0:
        return False

    if len(nums) == 1:
        return nums[0] == target

    if try_solve(nums[:-1], target - nums[-1], concat):
        return True

    if concat:
        n = len(str(nums[-1]))
        t = str(target)

        if n < len(t) and t[-n:] == str(nums[-1]) and try_solve(nums[:-1], int(t[0:-n]), concat):
            return True

    if target % nums[-1] != 0:
        return False

    return try_solve(nums[:-1], target // nums[-1], concat)


def part1(x):
    res = 0
    for line in x.split('\n'):
        target, nums = parse_line(line)
        if try_solve(nums, target):
            res += target

    return res


def part2(x):
    res = 0
    for line in x.split('\n'):
        target, nums = parse_line(line)
        if try_solve(nums, target, True):
            res += target

    return res


if __name__ == "__main__":
    part1_test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 3749
    assert part2(part2_test) == 11387

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
