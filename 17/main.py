from util import *


def run_vm(B, a, b, c):
    pc = 0

    def comb():
        v = B[pc+1]
        if 0 <= v <= 3:
            return v
        if 4 <= v <= 6:
            return [a, b, c][v-4]
        assert False

    res = []

    while pc < len(B):
        o = B[pc]

        if o == 0:
            a = int(a / (2**comb()))
            pc += 2
        elif o == 1:
            b ^= B[pc+1]
            pc += 2
        elif o == 2:
            b = comb() % 8
            pc += 2
        elif o == 3:
            if a == 0:
                pc += 2
            else:
                pc = B[pc+1]
        elif o == 4:
            b ^= c
            pc += 2
        elif o == 5:
            res.append(comb() % 8)
            pc += 2
        elif o == 6:
            b = int(a / (2**comb()))
            pc += 2
        else:
            assert o == 7
            c = int(a / (2**comb()))
            pc += 2

    return ','.join(map(str, res))


def part1(x):
    la, lb, lc, _, p = lines(x)
    a, = read_ints(la)
    b, = read_ints(lb)
    c, = read_ints(lc)

    B = list(read_ints(p))

    return run_vm(B, a, b, c)


def loop(a):
    b = a % 8
    b ^= 3
    c = a >> b
    b ^= 5
    b ^= c
    return b % 8


def dfs(b_rev, a0):
    if not b_rev:
        return a0

    for i in range(0, 8):
        a = (a0 << 3) + i
        if loop(a) != b_rev[0]:
            continue
        a1 = dfs(b_rev[1:], a)
        if a1 is not None:
            return a1

    return None


def part2(x):
    _, _, _, _, p = lines(x)

    B = list(read_ints(p))
    B = B[::-1]

    res = dfs(B, 0)
    assert run_vm(B[::-1], res, 0, 0) == ','.join(map(str, B[::-1]))
    return res


if __name__ == "__main__":
    part1_test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == "4,6,3,5,6,3,5,2,1,0"

    print("Part 1:", part1(test_file))

    # no tests for p2 - trust
    print("Part 2:", part2(test_file))
