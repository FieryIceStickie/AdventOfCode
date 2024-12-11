from math import comb
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    grid = {
        x+1j*y
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
        if v == '.' or v == 'S' and (start := x+1j*y)
    }
    return grid, start


def part_a_solver(grid: set[complex], start: complex):
    locs = {start}
    for _ in range(64):
        locs = {
            z
            for loc in locs
            for d in (-1, 1j, 1, -1j)
            if (z := loc + d) in grid
        }
    return len(locs)


def zmod(z: complex, m: int) -> complex:
    return complex(z.real % m, z.imag % m)

def part_b_solver(grid: set[complex], start: complex):
    side_len = int(max(z.real for z in grid)) + 1
    grid = {z for x in range(side_len + 1) for y in range(side_len + 1) if (z := x+1j*y) not in grid}
    curr = {start}
    def sim(locs: set[complex]) -> set[complex]:
        return {
            z
            for loc in locs
            for d in (-1, 1j, 1, -1j)
            if zmod(z := loc + d, side_len) not in grid
        }

    for _ in range(side_len // 2):
        curr = sim(curr)
    a = len(curr)
    for _ in range(side_len):
        curr = sim(curr)
    b = len(curr)
    for _ in range(side_len):
        curr = sim(curr)
    c = len(curr)
    g = b - a
    h = c - 2*b + a
    return a * comb(202300, 0) + g * comb(202300, 1) + h * comb(202300, 2)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    print(part_a_solver(*data))
    print(part_b_solver(*data))
