from collections import defaultdict

from util import *


def part1(x, k):
    nums = list(map(int, x.split(' ')))

    for i in range(0, k):
        nl = []

        for n in nums:
            if n == 0:
                nl.append(1)
                continue

            s = str(n)
            if len(s) % 2 == 0:
                nl.append(int(s[0:len(s)//2]))
                nl.append(int(s[len(s)//2:]))
                continue

            nl.append(2024*n)

        nums = nl

    return len(nums)


cache = {}


def part2(x, k):
    nd = defaultdict(lambda: 0)

    for n in map(int, x.split(' ')):
        nd[n] += 1

    for i in range(0, k):
        nl = defaultdict(lambda: 0)

        for n, c in nd.items():
            if n in cache:
                for p in cache[n]:
                    nl[p] += c

                continue

            if n == 0:
                nl[1] += c
                cache[n] = (1,)
                continue

            s = str(n)
            if len(s) % 2 == 0:
                a = int(s[0:len(s)//2])
                b = int(s[len(s)//2:])

                cache[n] = (a, b)
                nl[a] += c
                nl[b] += c

                continue

            nl[2024*n] += c
            cache[n] = (2024*n,)

        nd = nl

    res = 0

    for k, v in nd.items():
        res += v

    return res


if __name__ == "__main__":
    part1_test = """125 17"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test, 25))
    print("Part 2 (test):", part2(part2_test, 25))

    assert part1(part1_test, 25) == 55312
    assert part2(part2_test, 25) == 55312

    print("Part 1:", part1(test_file, 25))
    print("Part 2:", part2(test_file, 75))
