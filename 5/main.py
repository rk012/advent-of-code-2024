from collections import defaultdict
from functools import cmp_to_key

from util import *


def parse(x):
    r, u = x.split('\n\n')

    rules = {}
    updates = []

    for line in r.split('\n'):
        a, b = line.split('|')
        a, b = int(a), int(b)

        if a in rules:
            rules[a].append(b)
        else:
            rules[a] = [b]

    for line in u.split('\n'):
        updates.append(list(map(int, line.split(','))))

    return rules, updates


def part1(x):
    r, u = parse(x)

    res = 0

    for nums in u:
        v = set()
        valid = True

        for n in nums:
            v.add(n)
            if n not in r:
                continue

            for k in r[n]:
                if k in v:
                    valid = False

            if not valid:
                break

        if valid:
            res += nums[(len(nums) - 1) // 2]

    return res


def part2(x):
    r, u = parse(x)

    res = 0

    for nums in u:
        v = set()
        valid = True

        for n in nums:
            v.add(n)
            if n not in r:
                continue

            for k in r[n]:
                if k in v:
                    valid = False

            if not valid:
                break

        if valid:
            continue

        # goofy ahh topological sort
        v = set(nums)
        d = defaultdict(lambda: 0)
        s = []

        for n in v:
            if n in r:
                for k in r[n]:
                    if k in v:
                        d[n] += 1

        while v:
            for n in v:
                if d[n] > 0:
                    continue

                s.append(n)
                v.remove(n)

                for k in v:
                    if k in r and n in r[k]:
                        d[k] -= 1

                break

        res += s[(len(s)-1)//2]

    return res


if __name__ == "__main__":
    part1_test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 143
    assert part2(part2_test) == 123

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
