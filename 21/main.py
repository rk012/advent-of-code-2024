from util import *


def paths(a, b, g):
    i0, j0 = a
    i1, j1 = b

    if i0 <= i1:
        vd = 'v' * (i1-i0)
    else:
        vd = '^' * (i0-i1)

    if j0 <= j1:
        hd = '>' * (j1-j0)
    else:
        hd = '<' * (j0-j1)

    if g[i1][j0] is not None:
        yield vd + hd

    if g[i0][j1] is not None:
        yield hd + vd


def diff_strlen(a, b, nums, dpad, np, kp, q, cache, start=True):
    if (a, b, start, q) in cache:
        return cache[(a, b, start, q)]

    res = None
    for p in paths(a, b, nums if start else dpad):
        nxt = build_strlen(p+'A', nums, dpad, np, kp, q-1, False, cache)
        if res is None or nxt < res:
            res = nxt
    assert res is not None
    cache[(a, b, start, q)] = res
    return res


def build_strlen(x, nums, dpad, np, kp, q, start=True, cache=None):
    if q == 0:
        return len(x)

    if cache is None:
        cache = {}

    p = np if start else kp

    res = 0
    lc = 'A'
    for c in x:
        if c != lc:
            res += diff_strlen(p[lc], p[c], nums, dpad, np, kp, q, cache, start)
            lc = c
        else:
            # A
            res += 1

    # assert backtest(nums, dpad, res, p['A'], kp['A'], q, start) == x
    return res


def backtest(nums, dpad, x, v0, k0, q, start):
    if q == 0:
        return x

    g = nums if start else dpad

    dirs = "^>v<"
    i, j = v0
    res = ""

    for c in backtest(nums, dpad, x, k0, k0, q-1, False):
        if c == 'A':
            res += g[i][j]
            continue
        dx, dy = dir_dxy(dirs.find(c))
        i += dy
        j += dx
        assert g[i][j] is not None

    return res


def part1(x):
    nums = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A'],
    ]

    dpad = [
        [None, '^', 'A'],
        ['<', 'v', '>']
    ]

    np = {}
    kp = {}

    for i, j in grid_iter(nums):
        if nums[i][j] is not None:
            np[nums[i][j]] = (i, j)

    for i, j in grid_iter(dpad):
        if dpad[i][j] is not None:
            kp[dpad[i][j]] = (i, j)

    res = 0

    for r in lines(x):
        v3 = build_strlen(r, nums, dpad, np, kp, 3)
        res += v3 * list(read_ints(r))[0]

    return res


def part2(x):
    nums = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A'],
    ]

    dpad = [
        [None, '^', 'A'],
        ['<', 'v', '>']
    ]

    np = {}
    kp = {}

    for i, j in grid_iter(nums):
        if nums[i][j] is not None:
            np[nums[i][j]] = (i, j)

    for i, j in grid_iter(dpad):
        if dpad[i][j] is not None:
            kp[dpad[i][j]] = (i, j)

    res = 0

    for r in lines(x):
        v3 = build_strlen(r, nums, dpad, np, kp, 26)
        res += v3 * list(read_ints(r))[0]

    return res


if __name__ == "__main__":
    part1_test = """029A
980A
179A
456A
379A"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 126384

    print("Part 1:", part1(test_file))

    # p2_tst = part2(part2_test)
    # print("Part 2 (test):", p2_tst)

    # assert p2_tst ==

    print("Part 2:", part2(test_file))
