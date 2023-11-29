from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return [[*map(int, row.split('x'))] for row in raw_data.read().splitlines()]


def part_a_solver(data: list[list[int]]):
    return sum(2*(x*y + y*z + x*z) + x*y*z//max(x, y, z) for x, y, z in data)


def part_b_solver(data: list[list[int]]):
    return sum(x*y*z + 2*(x+y+z-max(x, y, z)) for x, y, z in data)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day2/day_2.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
