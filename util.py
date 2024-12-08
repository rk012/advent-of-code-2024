def read_str(fname):
    with open(fname, 'r') as f:
        return f.read()


def lines(x):
    return x.split('\n')


def cgrid(x):
    grid = []

    for row in lines(x):
        r = []
        for c in row:
            r.append(c)
        grid.append(row)

    return grid
