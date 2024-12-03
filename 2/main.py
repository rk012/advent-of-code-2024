from util import *


def parse_report(s):
    res = []
    for line in s.split('\n'):
        res.append(list(map(int, line.split(' '))))
    return res


def chk_nums(nums):
    flag = True
    incr = nums[0] < nums[1]
    for a, b in zip(nums, nums[1:]):
        if -3 <= a-b <= 3 and a != b and (a < b) == incr:
            continue

        flag = False
        break

    return flag


def part1(x):
    i = 0

    for nums in parse_report(x):
        if chk_nums(nums):
            i += 1

    return i


def chk_nums_damp(nums):
    if chk_nums(nums):
        return True, False, nums[0] < nums[1]

    for i in range(0, len(nums)+1):
        if chk_nums(nums[0:i] + nums[i+1:]):
            if i > 1:
                incr = nums[0] < nums[1]
            else:
                incr = nums[2] < nums[3]

            return True, True, incr

    return False, False, False


def part2(x):
    c = 0

    for nums in parse_report(x):
        flag, rem, incr = chk_nums_damp(nums[0:5])
        if not flag:
            continue

        last = nums[4]

        for i, n in enumerate(nums[5:]):
            safe = -3 <= last-n <= 3 and last != n and incr == (last < n)

            if not safe and rem:
                flag = False
                break

            if not safe:
                rem = True
                continue

            last = n

        if flag:
            c += 1

    return c


if __name__ == "__main__":
    part1_test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 2
    assert part2(part2_test) == 4

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
