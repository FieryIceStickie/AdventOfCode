from math import log
from typing import TextIO

from Tools.Python.path_stuff import *
from Years.Tools.utils import try_int


def parser(raw_data: TextIO):
    _, (_, x, _), (_, y, _), *_ = (map(try_int, i.split()) for i in raw_data.read().splitlines())
    return x*y


def part_a_solver(num: int):
    return (4**int(log(num * 2/3 - 1, 4) + 1) - 1) * 2//3 - num


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
