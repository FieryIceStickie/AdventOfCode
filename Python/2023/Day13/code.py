from io import StringIO
from typing import TextIO

import numpy as np

from Python.path_stuff import *


def parser(raw_data: TextIO):
    # noinspection PyTypeChecker
    return [
        np.genfromtxt(StringIO(grid), delimiter=1, dtype=np.str_, comments=None) == '#'
        for grid in raw_data.read().split('\n\n')
    ]


def part_a_solver(data):
    return sum(
        next((
            col
            for col in range(1, grid.shape[1])
            if np.array_equal(
                np.flip(grid[:, col - (size := min(col, grid.shape[1] - col)):col], 1),
                grid[:, col: col + size]
            )), 0
        )
        or
        100 * next(
            row
            for row in range(1, grid.shape[0])
            if np.array_equal(
                np.flip(grid[row - (size := min(row, grid.shape[0] - row)):row], 0),
                grid[row: row + size]
            )
        )
        for grid in data
    )


def part_b_solver(data):
    return sum(
        next((
            col
            for col in range(1, grid.shape[1])
            if np.count_nonzero(
                np.flip(grid[:, col - (size := min(col, grid.shape[1] - col)):col], 1) !=
                grid[:, col: col + size]
            ) == 1), 0
        )
        or
        100 * next(
            row
            for row in range(1, grid.shape[0])
            if np.count_nonzero(
                np.flip(grid[row - (size := min(row, grid.shape[0] - row)):row], 0) !=
                grid[row: row + size]
            ) == 1
        )
        for grid in data
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data), sep='\n\n')
    print(part_b_solver(data))
