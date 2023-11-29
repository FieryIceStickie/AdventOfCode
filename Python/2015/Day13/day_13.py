import re
from collections import defaultdict
from itertools import chain, islice, permutations
from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    graph = defaultdict(dict)
    for row in raw_data.read().splitlines():
        a, s, d, b = re.match(r'(\w).+(n|e) (\d+).+\s(\w).+$', row).groups()
        d = int(d) * (-1) ** (s == 'e')
        graph[a][b] = d
    return graph


def part_a_solver(graph: defaultdict[str, dict[str, int]]):
    a = next(iter(graph))
    return max(
        sum(graph[i][j] + graph[j][i] for i, j in zip(chain(a, p), chain(p, a)))
        for p in permutations(islice(graph, 1, None))
    )


def part_b_solver(graph: defaultdict[str, dict[str, int]]):
    return max(
        sum(graph[i][j] + graph[j][i] for i, j in zip(p, p[1:]))
        for p in permutations(graph)
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day13/day_13.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
