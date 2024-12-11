from typing import TextIO

from Tools.Python.path_stuff import *
from src.Tools.utils import deltas


def parser(raw_data: TextIO):
    grid = {}
    for x, row in enumerate(raw_data.read().splitlines()):
        for y, v in enumerate(row):
            grid[x+1j*y] = '#.v>^<'.find(v)
    return grid, x, y

def solver(grid: dict[complex, int], x_max: int, y_max: int) -> tuple[int, int]:
    start = 1j
    end = complex(x_max, y_max - 1)
    grid[-1+1j] = 0
    grid[end + 1] = 0
    # hardcoded prev_dir = 1
    active = [(start, start + 1, 1, False, 1)]
    p1_graph = {start: {}}
    p2_graph = {start: {}}
    while active:
        node, loc, prev_dir, is_directed, cost = active.pop()
        if loc in p1_graph:
            p1_graph[node][loc] = cost
            if not is_directed:
                p1_graph[loc][node] = cost
            p2_graph[node][loc] = cost
            p2_graph[loc][node] = cost
            continue
        candidates = [(z, d, v) for d in deltas if -d != prev_dir and (v := grid[z := loc + d])]
        if not candidates:
            p1_graph[loc] = {}
            p2_graph[loc] = {}
            p1_graph[node][loc] = cost
            if not is_directed:
                p1_graph[loc][node] = cost
            p2_graph[node][loc] = cost
            p2_graph[loc][node] = cost
        elif len(candidates) > 1:
            p1_graph[loc] = {}
            p2_graph[loc] = {}
            p1_graph[node][loc] = cost
            if not is_directed:
                p1_graph[loc][node] = cost
            p2_graph[node][loc] = cost
            p2_graph[loc][node] = cost
            for z, d, v in candidates:
                if v == 1:
                    active.append((loc, z, d, False, 1))
                elif d == 1j ** (v - 2):
                    active.append((loc, z + d, d, True, 2))
        else:
            # noinspection PyTypeChecker
            (z, d, v), = candidates
            if v == 1:
                active.append((node, z, d, is_directed, cost + 1))
            elif d == 1j ** (v - 2):
                active.append((node, z, d, True, cost + 1))
            else:
                raise ValueError
    pseudonyms = {z: i for i, z in enumerate(p1_graph)}
    p1_graph, p2_graph = tuple(
        {pseudonyms[k]: {pseudonyms[node]: cost for node, cost in v.items()} for k, v in graph.items()}
        for graph in (p1_graph, p2_graph)
    )
    end = pseudonyms[end]

    def dfs(graph: dict[int, dict[int, int]], node: int = 0) -> int:
        if node == end:
            return 0
        neighbours = graph.pop(node)
        c_max = None
        for loc, cost in neighbours.items():
            if loc in graph:
                rtn = dfs(graph, loc)
                if rtn is not None:
                    c_max = max(c_max, cost + rtn) if c_max is not None else cost + rtn
        graph[node] = neighbours
        return c_max
    return dfs(p1_graph), dfs(p2_graph)



if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(*data))