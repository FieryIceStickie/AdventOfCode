from typing import TextIO
from collections import Counter
import numpy as np

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return zip(*[map(int, line.split()) for line in raw_data.read().splitlines()])


def part_a_solver(left: list[int], right: list[int]):
    return int(np.linalg.norm(np.sort(left) - np.sort(right), ord=1))


def part_b_solver(left: list[int], right: list[int]):
    c = Counter(right)
    return sum(n * c[n] for n in left)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        left, right = parser(file)

    print(part_a_solver(left, right))
    print(part_b_solver(left, right))
