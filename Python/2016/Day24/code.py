from collections import deque
from functools import reduce
from itertools import permutations
from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    grid = {}
    goals = {}
    for x, row in enumerate(raw_data.read().splitlines()):
        for y, v in enumerate(row):
            z = x + 1j*y
            if v.isdigit():
                goals[int(v)] = z
            grid[z] = v == '#'
    return grid, [v for k, v in sorted(goals.items())]


def bfs(start: complex, ends: set[complex], grid: dict[complex, bool]) -> dict[complex, int]:
    active = deque([(start, 0)])
    visited = {start}
    rtn = {}
    while active:
        loc, steps = active.popleft()
        if loc in ends:
            ends -= {loc}
            rtn[loc] = steps
            if not ends:
                break
        candidates = [(z, steps + 1) for d in (-1, 1j, 1, -1j)
                      if not grid[z := loc + d] and z not in visited]
        visited |= {loc for loc, _ in candidates}
        active.extend(candidates)
    else:
        raise ValueError(f'no path to {ends}')
    return rtn


def get_graph(grid: dict[complex, bool], goals: list[complex]) -> tuple[int, dict[int, dict[int, int]]]:
    node_count = len(goals)
    graph = {i: {} for i in range(node_count)}
    for i, v in enumerate(goals[:-1]):
        nodes = goals[i + 1:]
        distances = bfs(v, {*nodes}, grid)
        for j, loc in enumerate(nodes, start=i + 1):
            graph[i][j] = graph[j][i] = distances[loc]
    return node_count, graph


def part_a_solver(node_count: int, graph: dict[int, dict[int, int]]):
    return min(reduce(lambda x, y: (x[0] + graph[x[1]][y], y), i, (0, 0))[0]
               for i in permutations(range(1, node_count)))


def part_b_solver(node_count: int, graph: dict[int, dict[int, int]]):
    return min(reduce(lambda x, y: (x[0] + graph[x[1]][y], y), (*i, 0), (0, 0))[0]
               for i in permutations(range(1, node_count)))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        grid, goals = parser(file)

    node_count, graph = get_graph(grid, goals)
    print(part_a_solver(node_count, graph))
    print(part_b_solver(node_count, graph))
