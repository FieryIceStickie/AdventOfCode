from typing import TextIO
from math import prod, sqrt, ceil, floor
from itertools import starmap

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return [*zip(*[map(int, line.split()[1:]) for line in raw_data.read().splitlines()])]


def part_a_solver(data: list[tuple[int, int]]):
    return prod(starmap(solve, data))

def solve(t: int, d: int) -> int:
    discrim = sqrt(t*t-4*d)
    return ceil(t/2 + discrim/2) - floor(t/2 - discrim/2) - 1

def part_b_solver(data: list[tuple[int, int]]):
    t, d = (int(''.join(map(str, c))) for c in zip(*data))
    return solve(t, d)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
