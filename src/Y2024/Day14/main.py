from collections import defaultdict
from typing import TextIO
import re
from itertools import batched, count
import numpy as np
from math import prod

from Tools.Python.path_stuff import *
from Tools.Python.utils import display_visited


def parser(raw_data: TextIO):
    return [
        *batched(map(int, re.findall(r'-?\d+', raw_data.read())), 4)
    ]


def sim(px, py, vx, vy, n):
    return (px + vx * n) % w, (py + vy * n) % h


def part_a_solver(data: list[tuple[int, int, int, int]]):
    grid = np.zeros((h, w), dtype=int)
    for px, py, vx, vy in data:
        x, y = sim(px, py, vx, vy, 100)
        grid[y, x] += 1
    w2, h2 = w // 2, h // 2
    return prod(map(np.sum, [grid[:h2, :w2], grid[h2+1:, :w2], grid[:h2, w2+1:], grid[h2+1:, w2+1:]]))


def part_b_solver(data: list[tuple[int, int, int, int]]):
    tree = {
        m+1j*d
        for d in range(4)
        for m in range(-d, d+1)
    } | {-2+4j, -1+4j, 1+4j, 2+4j}
    for s in count(0):
        grid = {
            complex(*sim(px, py, vx, vy, s))
            for px, py, vx, vy in data
        }
        if any(
            z for z in grid
            if {z+d for d in tree}.issubset(grid)
        ):
            display_visited(grid)
            return s


if __name__ == '__main__':
    testing = False
    w, h = (11, 7) if testing else (101, 103)

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
