import itertools

from util import *


def part1(x):
    mp, moves = x.split("\n\n")
    grid = cgrid(mp)

    x, y = 0, 0
    h, w = dims(grid)

    for i, j in itertools.product(range(0, h), range(0, w)):
        if grid[i][j] == '@':
            x, y = j, i
            break

    for m in moves:
        if m == '\n':
            continue

        dir = "^>v<".find(m)

        dx, dy = dir_dxy(dir)

        mv = True
        bl = False
        cx, cy = x+dx, y+dy

        while True:
            if grid[cy][cx] == '#':
                mv = False
                break

            if grid[cy][cx] == '.':
                if bl:
                    grid[cy][cx] = 'O'
                break

            assert grid[cy][cx] == 'O'
            bl = True
            cx += dx
            cy += dy

        if mv:
            grid[y][x] = '.'
            x, y = x+dx, y+dy
            grid[y][x] = '@'

    res = 0

    for i in range(0, h):
        for j in range(0, w):
            if grid[i][j] != 'O':
                continue

            res += 100*i + j

    return res


def chk_move(grid, cx, cy, dx, dy, sd=True):
    assert in_grid(cy, cx, grid)
    c = grid[cy][cx]
    if c == '.':
        return True
    if c == '#':
        return False

    alt = True

    if c == '[' and dx == 0 and sd:
        alt = chk_move(grid, cx + 1, cy, dx, dy, False)
    elif c == ']' and dx == 0 and sd:
        alt = chk_move(grid, cx - 1, cy, dx, dy, False)

    return alt and chk_move(grid, cx + dx, cy + dy, dx, dy)


def mk_move(grid, cx, cy, dx, dy, sd=True):
    c = grid[cy][cx]
    assert c in "@.[]"

    if c == '.':
        return

    if c == '[' and dx == 0 and sd:
        mk_move(grid, cx+1, cy, dx, dy, False)
        grid[cy][cx+1] = '.'
    elif c == ']' and dx == 0 and sd:
        mk_move(grid, cx-1, cy, dx, dy, False)
        grid[cy][cx-1] = '.'

    mk_move(grid, cx+dx, cy+dy, dx, dy)
    grid[cy+dy][cx+dx] = grid[cy][cx]


def part2(x):
    mp, moves = x.split("\n\n")
    og = cgrid(mp)

    grid = []

    for r in og:
        cr = []
        for c in r:
            if c == 'O':
                cr += ['[', ']']
            elif c == '@':
                cr += ['@', '.']
            else:
                cr += [c, c]
        grid.append(cr)

    x, y = 0, 0
    h, w = dims(grid)

    for i, j in itertools.product(range(0, h), range(0, w)):
        if grid[i][j] == '@':
            x, y = j, i
            break

    for m in moves:
        if m == '\n':
            continue

        dir = "^>v<".find(m)
        assert grid[y][x] == '@'

        dx, dy = dir_dxy(dir)

        cx, cy = x+dx, y+dy

        if chk_move(grid, cx, cy, dx, dy):
            mk_move(grid, x, y, dx, dy)
            grid[y][x] = '.'
            x, y = cx, cy

    res = 0

    for i in range(0, h):
        for j in range(0, w):
            if grid[i][j] != '[':
                continue

            res += 100*i + j

    return res


if __name__ == "__main__":
    part1_test = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert part1(part1_test) == 10092

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test)
    print("Part 2 (test):", part2(part2_test))

    assert part2(part2_test) == 9021

    print("Part 2:", part2(test_file))
