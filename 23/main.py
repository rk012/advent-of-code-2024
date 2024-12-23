from util import *


def part1(x):
    edges = []
    for l in lines(x):
        a, b = l.split('-')
        edges.append((a, b))

    verts = set()

    for a, b in edges:
        verts.add(a)
        verts.add(b)

    g = Graph(verts, False)

    for a, b in edges:
        g.add_edge(a, b)

    triples = set()

    for a, b in g.edges.keys():
        for v in verts:
            if (a, v) in g.edges and (b, v) in g.edges:
                triples.add((a, b, v))

    res = 0

    for a, b, c in triples:
        if a[0] == 't' or b[0] == 't' or c[0] == 't':
            res += 1

    return res // 6


def vdfs(g, verts, av):
    n = len(verts)
    s = verts.copy()

    avn = av.copy()

    for v in av:
        flag = True
        for u in verts:
            if (u, v) not in g.edges:
                flag = False
                break

        if not flag:
            continue

        verts.add(v)
        avn.remove(v)
        a = vdfs(g, verts, avn)

        verts.remove(v)
        if len(a) > n:
            s = a.copy()
            n = len(a)

    return s


def part2(x):
    edges = []
    for l in lines(x):
        a, b = l.split('-')
        edges.append((a, b))

    verts = set()

    for a, b in edges:
        verts.add(a)
        verts.add(b)

    g = Graph(verts, False)

    for a, b in edges:
        g.add_edge(a, b)

    res = set()

    for i, av in enumerate(g.components()):
        a = vdfs(g, set(), av)
        if len(a) > len(res):
            res = a

    return ','.join(sorted(res))



if __name__ == "__main__":
    part1_test = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

    part2_test = part1_test

    test_file = read_str("input.txt")

    p1_tst = part1(part1_test)
    print("Part 1 (test):", p1_tst)

    assert p1_tst == 7

    print("Part 1:", part1(test_file))

    p2_tst = part2(part2_test)
    print("Part 2 (test):", p2_tst)

    assert p2_tst == "co,de,ka,ta"

    print("Part 2:", part2(test_file))
