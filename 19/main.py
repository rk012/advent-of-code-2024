from util import *


def pdfs(p, pttrns):
    if p == "":
        return True

    for i in range(1, len(p)+1):
        if p[0:i] in pttrns and pdfs(p[i:], pttrns):
            return True
    return False


def part1(x):
    towels, pattrns = x.split("\n\n")
    towels = set(towels.split(', '))
    pattrns = lines(pattrns)

    res = 0

    for p in pattrns:
        if pdfs(p, towels):
            res += 1

    return res


cache = {}


def pdfs2(p, pttrns):
    if p == "":
        return 1

    if p in cache:
        return cache[p]

    res = 0

    for i in range(1, len(p)+1):
        if p[0:i] in pttrns:
            res += pdfs2(p[i:], pttrns)

    cache[p] = res
    return res


def part2(x):
    towels, pattrns = x.split("\n\n")
    towels = set(towels.split(', '))
    pattrns = lines(pattrns)

    res = 0

    for p in pattrns:
        res += pdfs2(p, towels)

    global cache
    cache = {}
    return res


if __name__ == "__main__":
    part1_test = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 6

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test)
    print("Part 2 (test):", p2_tst)

    assert p2_tst == 16

    print("Part 2:", part2(test_file))
