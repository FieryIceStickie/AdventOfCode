import heapq
from typing import TextIO

import numpy as np

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [
        ((x0, x1), (y0, y1), (z0, z1))
        for (x0, y0, z0), (x1, y1, z1) in
        ([map(int, nums.split(',')) for nums in line.split('~')]
         for line in raw_data.read().splitlines())
    ]

def solver(bricks: list[tuple[tuple[int, int], ...]]):
    graph = {i: [set(), set()] for i in range(len(bricks))}
    grid_width, grid_height = max(x for (_, x), *_ in bricks) + 1, max(y for _, (_, y), _ in bricks) + 1
    height_grid = np.zeros((grid_width, grid_height), dtype=np.uint16)
    brick_grid = np.zeros((grid_width, grid_height), dtype=np.uint16)
    bricks.sort(key=lambda b: b[-1][0])
    for brick_idx, ((x0, x1), (y0, y1), (z0, z1)) in enumerate(bricks):
        max_height = np.max(height_grid[x0:x1+1, y0:y1+1])
        if max_height:
            bricks_x, bricks_y = np.nonzero(height_grid[x0:x1+1, y0:y1+1] == max_height)
            bricks_x += x0
            bricks_y += y0
            graph[brick_idx][0] |= {*brick_grid[bricks_x, bricks_y]}
        new_z = 1 + max_height
        new_brick = (x0, x1), (y0, y1), (new_z, new_z - z0 + z1)
        bricks[brick_idx] = new_brick
        height_grid[x0:x1+1, y0:y1+1] = new_z - z0 + z1
        brick_grid[x0:x1+1, y0:y1+1] = brick_idx
    for brick_idx, (below, _) in graph.items():
        for idx in below:
            graph[idx][1].add(brick_idx)
    p1 = p2 = 0
    for brick_idx in graph:
        active = [(bricks[brick_idx][-1][0], brick_idx)]
        seen = set()
        while active:
            _, node = heapq.heappop(active)
            seen.add(node)
            for idx in graph[node][1]:
                if all(i in seen for i in graph[idx][0]):
                    heapq.heappush(active, (bricks[idx][-1][0], idx))
        p1 += len(seen) == 1
        p2 += len(seen) - 1
    return p1, p2


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(data))
