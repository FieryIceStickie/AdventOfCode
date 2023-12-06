from typing import TextIO
from math import prod, sqrt

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return [*zip(*[map(int, line.split()[1:]) for line in raw_data.read().splitlines()])]


def part_a_solver(data):
    return prod(
        int(t/2 + sqrt(t*t-4*d)/2) - int(t/2 - sqrt(t*t-4*d)/2)
        for t, d in data
    )


def part_b_solver(data):
    t, d = (int(''.join(map(str, c))) for c in zip(*data))
    return int(t/2 + sqrt(t*t-4*d)/2) - int(t/2 - sqrt(t*t-4*d)/2)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
