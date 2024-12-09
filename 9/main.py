from util import *


def part1(x):
    d = []
    i = 0
    f = True
    for c in x:
        n = int(c)
        if f:
            d += n*[i]
            i += 1
        else:
            d += list(n*'.')

        f = not f

    i = 0

    while i < len(d) and d[i] != '.':
        i += 1

    j = len(d)-1

    while j >= 0 and d[j] == '.':
        j -= 1

    while i < j:
        d[i] = d[j]
        d[j] = '.'

        while j >= 0 and d[j] == '.':
            j -= 1

        while i < len(d) and d[i] != '.':
            i += 1

    res = 0

    for i, c in enumerate(d):
        if c == '.':
            continue

        res += i*c

    return res


def part2(x):
    d = []
    i = 0
    f = True
    for c in x:
        n = int(c)
        if f:
            d += n*[i]
            i += 1
        else:
            d += list(n*'.')

        f = not f

    i = 0

    while i < len(d):
        while i < len(d) and d[i] != '.':
            i += 1

        n = 0
        while i < len(d) and d[i] == '.':
            i += 1
            n += 1

        if n == 0:
            break

        j = len(d) - 1
        while i <= j:
            while i <= j and d[j] == '.' or d[j] == 'X':
                j -= 1

            m = 0
            a = d[j]
            while i <= j and d[j] == a:
                j -= 1
                m += 1

            if m == 0:
                break

            # copy
            if n < m:
                continue

            for q in range(0, m):
                d[i-n+q] = d[j+q+1]
                d[j+q+1] = 'X'

            i -= n
            break

    res = 0

    for i, c in enumerate(d):
        if c == '.' or c == 'X':
            continue

        res += i*c

    return res


if __name__ == "__main__":
    part1_test = """2333133121414131402"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 1928
    assert part2(part2_test) == 2858

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
