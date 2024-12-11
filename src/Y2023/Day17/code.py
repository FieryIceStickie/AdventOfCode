import heapq
from collections import defaultdict
from functools import partial
from typing import TextIO

import numpy as np

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return np.genfromtxt(raw_data, delimiter=1, dtype=np.int8)


# noinspection PyTypeChecker
def z_index(arr: np.ndarray, z: complex) -> int:
    return int(arr[int(z.real), int(z.imag)])


def part_a_solver(grid: np.ndarray):
    get_cost = partial(z_index, grid)

    def is_valid(z: complex) -> bool:
        return grid.shape[0] > z.real >= 0 <= z.imag < grid.shape[1]

    x, y = grid.shape
    end = complex(x-1, y-1)
    visited = defaultdict(lambda: [np.inf] * 4)
    active = [(get_cost(1j), 0, 1j, 1j, 0), (get_cost(1), 1, 1, 1, 0)]
    counter = 2
    while active:
        cost, _, loc, facing, cumulant = heapq.heappop(active)

        if loc == end:
            break

        node_state = visited[loc, facing]
        if cost >= node_state[cumulant]:
            continue

        for idx in range(cumulant, 3):
            if node_state[idx] <= cost:
                break
            node_state[idx] = cost

        if cumulant < 2 and is_valid(z := loc + facing):
            heapq.heappush(active, (cost + get_cost(z), counter, z, facing, cumulant+1))
            counter += 1
        for d in (1j, -1j):
            new_facing = facing * d
            if is_valid(z := loc + new_facing):
                heapq.heappush(active, (cost + get_cost(z), counter, z, new_facing, 0))
                counter += 1
    return cost


def part_b_solver(grid: np.ndarray):
    get_cost = partial(z_index, grid)

    def is_valid(z: complex) -> bool:
        return grid.shape[0] > z.real >= 0 <= z.imag < grid.shape[1]

    x, y = grid.shape
    end = complex(x - 1, y - 1)
    visited = defaultdict(lambda: [np.inf] * 7)
    active = [(sum(get_cost(1j*i) for i in range(1, 5)), 0, 4j, 1j, 0),
              (sum(get_cost(i) for i in range(1, 5)), 1, 4, 1, 0)]
    counter = 2
    while active:
        cost, _, loc, facing, cumulant = heapq.heappop(active)

        if loc == end:
            break

        node_state = visited[loc, facing]
        if cost >= node_state[cumulant]:
            continue

        for idx in range(cumulant, 3):
            if node_state[idx] <= cost:
                break
            node_state[idx] = cost

        if cumulant < 6 and is_valid(z := loc + facing):
            heapq.heappush(active, (cost + get_cost(z), counter, z, facing, cumulant + 1))
            counter += 1
        for d in (1j, -1j):
            new_facing = facing * d
            if is_valid(z := loc + 4*new_facing):
                heapq.heappush(active,
                               (cost + sum(get_cost(loc+i*new_facing) for i in range(1, 5)),
                                counter, z, new_facing, 0))
                counter += 1
    return cost


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
