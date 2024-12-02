from typing import TextIO

from Tools.Python.path_stuff import *

from itertools import pairwise

from math import ceil
from Tools.Python.utils import sgn


def parser(raw_data: TextIO):
    return [[*map(int, line.split())] for line in raw_data.read().splitlines()]


def diff(arr: list[int]):
    return [j - i for i, j in pairwise(arr)]


def is_good(level: list[int]):
    scaled_diffs = [sgn(d) * ceil(abs(d) / 3) for d in diff(level)]
    print(diff(level), scaled_diffs)
    sign = scaled_diffs[0]
    return abs(sign) == 1 and all(d == sign for d in scaled_diffs)


def full_solver(levels: list[list[int]]):
    p1 = p2 = 0
    for level in levels:
        if is_good(level):
            p1 += 1
            p2 += 1
        elif any(
            is_good(level[:i] + level[i+1:])
            for i in range(len(level))
        ):
            p2 += 1
    return p1, p2


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(data))
