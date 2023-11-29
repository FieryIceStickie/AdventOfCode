from collections import Counter
from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data: list[str]):
    return ''.join(Counter(s).most_common(1)[0][0] for s in zip(*data))


def part_b_solver(data: list[str]):
    return ''.join(Counter(s).most_common()[-1][0] for s in zip(*data))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
