from util import *


def gen(x):
    while True:
        x = ((x*64) ^ x) % 16777216
        x = ((x // 32) ^ x) % 16777216
        x = ((x*2048) ^ x) % 16777216

        yield x


def changes(x):
    res = []
    l = None
    for i, n in enumerate(gen(x)):
        p = n % 10
        if l is None:
            l = p
            continue
        res.append(p-l)
        l = p

        if i == 2000:
            break
    assert len(res) == 2000
    return res


def get_price(x, seq):
    g = gen(x)
    p = [next(g) for i in range(0, 2000)]
    d = changes(x)

    buf = d[0:4]

    for i in range(4, 2000):
        if tuple(buf) == seq:
            return d[i]
        buf = buf[1:] + [p[i]]
        assert len(buf) == 4

    return 0


def part1(x):
    res = 0

    for n in lines(x):
        n = int(n)
        for i, h in enumerate(gen(n)):
            if i == 1999:
                res += h
                break

    return res


def part2(x):
    d = []

    for n in map(int, lines(x)):
        c = changes(n)
        g = gen(n)
        p = [next(g) % 10 for _ in range(0, 2000)]

        buf = c[0:4]
        h = {}

        for i in range(4, 2000):
            b = tuple(buf)
            if b not in h:
                h[b] = p[i]
            buf = buf[1:] + [c[i]]
            assert len(buf) == 4

        d.append(h)

    res = 0

    for p, q, r, s in itertools.product(range(-9, 10), range(-9, 10), range(-9, 10), range(-9, 10)):
        seq = (p, q, r, s)
        a = 0
        for h in d:
            if seq in h:
                a += h[seq]
        res = max(res, a)

    return res




if __name__ == "__main__":
    part1_test = """1
10
100
2024"""

    part2_test = """1
2
3
2024"""

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 37327623

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test)
    print("Part 2 (test):", p2_tst)

    assert p2_tst == 23

    print("Part 2:", part2(test_file))
