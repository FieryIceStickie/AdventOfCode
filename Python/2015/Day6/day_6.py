from typing import TextIO
import re

import numpy as np

from Python.path_stuff import *


def parser(raw_data: TextIO):
    res = []
    row_pattern = re.compile(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')
    for row in raw_data.read().splitlines():
        instruction, *data = row_pattern.match(row).groups()
        res.append((['turn off', 'turn on', 'toggle'].index(instruction), *map(int, data)))
    return res


def part_a_solver(data: list[tuple[int, ...]]):
    grid = np.zeros((1000, 1000), dtype=bool)
    for row in data:
        match row:
            case 0, a, b, c, d:
                grid[a:c+1, b:d+1] = 0
            case 1, a, b, c, d:
                grid[a:c+1, b:d+1] = 1
            case 2, a, b, c, d:
                grid[a:c+1, b:d+1] = ~grid[a:c+1, b:d+1]
    return np.count_nonzero(grid)


def part_b_solver(data: list[tuple[int, ...]]):
    grid = np.zeros((1000, 1000), dtype=int)
    for row in data:
        match row:
            case 0, a, b, c, d:
                grid[a:c + 1, b:d + 1] = grid[a:c + 1, b:d + 1] - (grid[a:c + 1, b:d + 1] != 0)
            case 1, a, b, c, d:
                grid[a:c + 1, b:d + 1] += 1
            case 2, a, b, c, d:
                grid[a:c + 1, b:d + 1] += 2
    return np.sum(grid)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day 6/day_6.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
