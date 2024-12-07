from util import *


def dir_dxy(dir):
    if dir == 0:
        return 0, -1
    elif dir == 1:
        return 1, 0
    elif dir == 2:
        return 0, 1
    else:
        return -1, 0


saved_grid: None | list[list[str]] = None
x0, y0 = 0, 0


def part1(x):
    grid = []
    visited = []

    for line in x.split('\n'):
        grid.append([line[i] for i in range(0, len(line))])
        visited.append([set() for _ in range(0, len(line))])

    i = ''.join(x.split('\n')).find('^')

    x = i % len(grid[0])
    y = i // len(grid[0])

    global x0, y0
    x0, y0 = x, y

    n = 0
    dir = 0

    while dir not in visited[y][x]:
        x1, y1 = x, y
        if dir == 0:
            y1 -= 1
        elif dir == 1:
            x1 += 1
        elif dir == 2:
            y1 += 1
        else:
            x1 -= 1

        visited[y][x].add(dir)

        if y1 < 0 or y1 >= len(grid) or x1 < 0 or x1 >= len(grid[0]):
            if grid[y][x] != 'X':
                n += 1
                grid[y][x] = 'X'
            break

        if grid[y1][x1] == '#':
            dir += 1
            dir %= 4
            continue

        if grid[y][x] != 'X':
            n += 1
            grid[y][x] = 'X'

        x, y = x1, y1

    global saved_grid
    saved_grid = grid

    return n


def is_loop():
    global saved_grid, x0, y0
    grid = saved_grid
    x, y = x0, y0

    visited = [[set() for _ in grid[0]] for _ in grid]
    dir = 0

    while dir not in visited[y][x]:
        dx, dy = dir_dxy(dir)
        x1, y1 = x+dx, y+dy

        visited[y][x].add(dir)

        if y1 < 0 or y1 >= len(grid) or x1 < 0 or x1 >= len(grid[0]):
            return False

        if grid[y1][x1] == '#':
            dir += 1
            dir %= 4
            continue

        x, y = x1, y1

    return True


def part2(x):
    # load saved grid, start pos
    part1(x)

    global saved_grid
    grid = saved_grid

    n = 0

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] != 'X':
                continue

            grid[i][j] = '#'
            if is_loop():
                n += 1
            grid[i][j] = 'X'

    return n


if __name__ == "__main__":
    part1_test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    part2_test = part1_test

    test_file = read_str("input.txt")

    print("Part 1 (test):", part1(part1_test))
    print("Part 2 (test):", part2(part2_test))

    assert part1(part1_test) == 41
    assert part2(part2_test) == 6

    print("Part 1:", part1(test_file))
    print("Part 2:", part2(test_file))
