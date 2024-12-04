from util import *


def rot_str(strs):
    n = len(strs[0])
    res = []

    for i in range(0, n):
        buf = ""
        for line in strs:
            buf += line[i]
        res.append(buf)

    return res


def diag_r(lines):
    n = len(lines[0])
    m = len(lines)
    res = []

    for i in range(0, n):
        buf = ""
        for j, line in enumerate(lines):
            if i+j >= n:
                break

            buf += line[i+j]
        res.append(buf)

    for i in range(1, m):
        buf = ""
        for j, line in enumerate(lines[i:]):
            if j >= n:
                break
            buf += line[j]
        res.append(buf)

    return res


def diag_l(lines):
    return diag_r(list(map(lambda x: x[::-1], lines)))


def count_xmas(s):
    count = 0

    for i, _ in enumerate(s[:-3]):
        if s[i:i+4] == "XMAS" or s[i:i+4] == "SAMX":
            count += 1

    return count


def find_mas(s):
    idx = []

    for i, _ in enumerate(s[:-2]):
        if s[i:i+3] == "MAS" or s[i:i+3] == "SAM":
            idx.append(i)

    return idx


def part1(x):
    grid = x.split('\n')
    rot = rot_str(grid)
    dl = diag_l(grid)
    dr = diag_r(grid)

    count = 0

    for lines in (grid, rot, dl, dr):
        for line in lines:
            count += count_xmas(line)

    return count


def part2(x):
    lines = x.split('\n')
    count = 0

    for i in range(0, len(lines)-2):
        for j in range(0, len(lines[0])-2):
            dr = lines[i][j] + lines[i+1][j+1] + lines[i+2][j+2]
            dl = lines[i][j+2] + lines[i+1][j+1] + lines[i+2][j]

            if (dl == "MAS" or dl == "SAM") and (dr == "MAS" or dr == "SAM"):
                count += 1

    return count


if __name__ == "__main__":
    part1_test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 18
    assert part2(part2_test) == 9

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
