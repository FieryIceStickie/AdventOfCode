import re
from collections import defaultdict
from itertools import pairwise, permutations
from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    graph = defaultdict(dict)
    pattern = re.compile(r'(\w+) to (\w+) = (\d+)')
    for row in raw_data.read().splitlines():
        city1, city2, dist = pattern.match(row).groups()
        graph[city1][city2] = graph[city2][city1] = int(dist)
    return graph


def part_a_solver(graph: dict[str, dict[str, int]]):
    return min(sum(graph[city1][city2] for city1, city2 in pairwise(path)) for path in permutations(graph))


def part_b_solver(graph: dict[str, dict[str, int]]):
    return max(sum(graph[city1][city2] for city1, city2 in pairwise(path)) for path in permutations(graph))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day9/day_9.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
