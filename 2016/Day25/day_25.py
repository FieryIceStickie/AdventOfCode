from typing import TextIO
from math import log
from Tools.utils import try_int

from path_stuff import *


def parser(raw_data: TextIO):
    _, (_, x, _), (_, y, _), *_ = (map(try_int, i.split()) for i in raw_data.read().splitlines())
    return x*y


def part_a_solver(num: int):
    return (4**int(log(num * 2/3 - 1, 4) + 1) - 1) * 2//3 - num


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 25/day_25.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
