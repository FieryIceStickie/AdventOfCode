from collections import defaultdict
from collections.abc import Callable
from typing import TextIO
from itertools import count
from attrs import define, field
import heapq

from Tools.Python.path_stuff import *
from Tools.Python.utils.utils import deltas

type Graph = dict[complex, dict[complex, tuple[tuple[complex, complex], int, int]]]
type LocFacing = tuple[complex, complex]


@define(order=True)
class PrioItem:
    cost: int
    num_tiles: int
    loc_facing: LocFacing = field(order=False)
    pred: LocFacing | None = field(order=False)


@define
class VisitedNode:
    cost: int
    tile_count: int = 0
    preds: set[LocFacing] = field(factory=set)


def parser(raw_data: TextIO):
    grid = {}
    for x, row in enumerate(raw_data.read().splitlines()):
        for y, v in enumerate(row):
            z = x + 1j * y
            if v == "S":
                start = z
            elif v == 'E':
                end = z
            grid[z] = v == '#'
    graph = collapse_grid(grid, {start, end})
    return graph, start, end


def collapse_grid(
    grid: dict[complex, bool],
    forced_nodes: set[complex]
) -> Graph:
    if not forced_nodes:
        start, d = next(
            (z, s.pop()) for z, v in grid.items()
            if not v and len(s := {
                d for d in deltas
                if not grid[z + d]
            }) == 1
        )
        active = [(start, d)]
    else:
        start = next(iter(forced_nodes))
        active = [(start, d) for d in deltas if not grid[start + d]]
    graph = {start: {}}
    visited = set()
    while active:
        node, orig_d = z, curr_d = active.pop()
        if (node, orig_d) in visited:
            continue
        num_turns = 0
        is_dead_end = False
        for num_tiles in count(1):
            z += curr_d
            if z in forced_nodes or len(s := {
                curr_d * d for d in (-1j, 1, 1j)
                if not grid[z + curr_d * d]
            }) > 1:  # do != 0 if you want to include dead-ends
                break
            elif not s:
                is_dead_end = True
                break
            if (new_d := s.pop()) != curr_d:
                curr_d = new_d
                num_turns += 1
        if is_dead_end:
            continue
        visited.add((node, orig_d))
        visited.add((z, -curr_d))
        graph[node][orig_d] = ((z, curr_d), num_tiles, num_turns)
        graph.setdefault(z, {})[-curr_d] = ((node, -orig_d), num_tiles, num_turns)
        active += [(z, d) for d in s]
    return graph


def manhattan(z: complex) -> int:
    return int(abs(z.real)) + int(abs(z.imag))


def get_h(end: complex, facings: set[complex]) -> Callable[[complex, complex], int]:
    """
    Heuristic for A*
    Note: After testing, this heuristic is worse than both manhattan and doing nothing,
    so in the actual function this isn't used
    :param end: end point
    :param facings: set of directions you can go at the end point
    """
    if len(facings) == 1:
        return lambda z, d: manhattan(end - z) + 1000 * (-d not in facings) * (1 + (d in facings))
    return lambda z, d: manhattan(end - z) + 1000 * (-d not in facings)


def count_tiles(visited: dict[LocFacing, VisitedNode], ends: set[LocFacing]) -> int:
    p2 = 0
    cache = defaultdict(set)

    def visit(node: LocFacing) -> None:
        if node is None:
            return
        nonlocal p2
        if node[1] in cache[node[0]]:
            return
        cache[node[0]].add(node[1])
        p2 += visited[node].tile_count
        for pred in visited[node].preds:
            visit(pred)

    for end in ends:
        visit(end)
    return p2 + len(cache)


def full_solver(graph: Graph, start: complex, end: complex):
    loc_facing = start, 1j
    active: list[PrioItem] = [PrioItem(0, 1, loc_facing, None)]
    visited: dict[LocFacing, VisitedNode] = {}
    p1 = None
    ends = set()
    iter_count = 0
    while active:
        iter_count += 1
        node: PrioItem = heapq.heappop(active)
        if p1 and node.cost > p1:
            break

        has_visited = False
        if node.loc_facing in visited:
            if visited[node.loc_facing].cost < node.cost:
                continue
            has_visited = True
        else:
            visited[node.loc_facing] = VisitedNode(node.cost)
        visited[node.loc_facing].preds.add(node.pred)
        visited[node.loc_facing].tile_count += node.num_tiles - 1
        if has_visited:
            continue

        if node.loc_facing[0] == end:
            p1 = node.cost
            ends.add(node.loc_facing)
            continue

        for facing, (new_loc_facing, num_tiles, num_turns) in graph[node.loc_facing[0]].items():
            if facing == node.loc_facing[1]:
                new_cost = node.cost + num_tiles + 1000 * num_turns
                new_num_tiles = num_tiles
            elif node.pred is None or node.loc_facing[0] != node.pred[0]:
                new_cost = node.cost + 1000
                new_loc_facing = node.loc_facing[0], facing
                new_num_tiles = 1
            else:
                continue
            if new_loc_facing in visited and visited[new_loc_facing].cost < new_cost:
                continue
            heapq.heappush(active, PrioItem(
                new_cost, new_num_tiles,
                new_loc_facing, node.loc_facing,
            ))
    else:
        raise ValueError('no valid path')
    # print(f'Iter count: {iter_count}')
    return p1, count_tiles(visited, ends)


if __name__ == '__main__':
    testing = False
    import time

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    st = time.perf_counter()
    print(*full_solver(*data))
    ed = time.perf_counter()
    print(ed - st)
