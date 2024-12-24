from collections import defaultdict, Counter
from typing import TextIO


def parser(raw_data: TextIO):
    graph = defaultdict(set)
    counts = {}
    for line in raw_data:
        u, v = line.strip().replace('t', 'T').split('-')
        if v < u: u, v = v, u
        graph[u].add(v)
        counts[u] = 0
        counts[v] = 0
    return graph, counts


def full_solver(graph: dict[str, set[str]], counts: dict[str, int]):
    p1 = 0
    for u, n1 in graph.items():
        for v in n1:
            for w in graph.get(v, set()):
                if w in n1:
                    counts[u] += 1
                    counts[v] += 1
                    counts[w] += 1
                    p1 += u.startswith('T')
    return p1, ','.join(sorted(s.lower() for s, n in counts.items() if n == 66))


if __name__ == '__main__':
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = 'input.txt'
    else:
        path = test_path if testing else 'input.txt'

    import time
    st = time.perf_counter()
    with open(path, 'r') as file:
        data = parser(file)

    print(*full_solver(*data))
    ed = time.perf_counter()
    print(ed - st)
