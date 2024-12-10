def read_str(fname):
    with open(fname, 'r') as f:
        return f.read()


def lines(x):
    return x.split('\n')


def cgrid(x, fn=lambda x: x):
    grid = []

    for row in lines(x):
        r = []
        for c in row:
            r.append(fn(c))
        grid.append(r)

    return grid
