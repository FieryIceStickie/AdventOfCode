from typing import TextIO

from Years.path_stuff import *

from itertools import pairwise


def parser(raw_data: TextIO):
    return [[*map(int, line.split())] for line in raw_data.read().splitlines()]


def diff(arr: list[int]):
    return [j - i for i, j in pairwise(arr)]


def part_a_solver(levels: list[list[int]]):
    return sum(
        1 for level in levels
        if 
    )


def part_b_solver(levels: list[list[int]]):
    return


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
