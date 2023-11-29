from typing import TextIO

from path_stuff import *

import scipy
import numpy as np
from numpy.typing import NDArray


def parser(raw_data: TextIO):
    return np.array([[v == '#' for v in line] for line in raw_data.read().splitlines()], dtype=np.uint8)


def part_a_solver(grid: NDArray[np.uint8]):
    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 9
    for _ in range(100 if not testing else 4):
        grid = np.isin(scipy.ndimage.convolve(grid, kernel, mode='constant'), (3, 11, 12)).astype(np.uint8)
    return np.count_nonzero(grid)


def part_b_solver(grid: NDArray[bool]):
    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 9
    for _ in range(100 if not testing else 4):
        grid = np.isin(scipy.ndimage.convolve(grid, kernel, mode='constant'), (3, 11, 12)).astype(np.uint8)
        grid[[0, 0, -1, -1], [0, -1, 0, -1]] = 1
    return np.count_nonzero(grid)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day 18/day_18.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
