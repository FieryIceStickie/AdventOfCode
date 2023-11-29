from typing import TextIO
from collections import Counter

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data: list[str]):
    return ''.join(Counter(s).most_common(1)[0][0] for s in zip(*data))


def part_b_solver(data: list[str]):
    return ''.join(Counter(s).most_common()[-1][0] for s in zip(*data))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day6/day_6.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
