from itertools import chain
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return [[*map(int, row.split())] for row in raw_data.read().splitlines()]


def part_a_solver(sides: list[list[int]]):
    return sum(1 for triangle in sides if sum(triangle) > 2 * max(triangle))


def part_b_solver(sides: list[list[int]]):
    return sum(1 for triangle in zip(*[iter(chain.from_iterable(zip(*sides)))]*3)
               if sum(triangle) > 2 * max(triangle))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
