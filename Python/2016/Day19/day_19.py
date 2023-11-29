from typing import TextIO
from math import log

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return int(raw_data.read())


def part_a_solver(num: int):
    return ((1 << (num.bit_length() - 1) ^ num) << 1) + 1


def part_b_solver(num: int):
    return max(min(n := 3 ** int(log(num, 3)), num - n), 0) + 2*max(num - 2*n, 0)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day19/day_19.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
