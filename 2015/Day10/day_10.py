from typing import TextIO
from itertools import groupby

from path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def solver(num: str):
    for _ in range(40):
        num = ''.join(f'{len(list(g))}{k}' for k, g in groupby(num))
    pt1 = len(num)
    for _ in range(10):
        num = ''.join(f'{len(list(g))}{k}' for k, g in groupby(num))
    return pt1, len(num)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day 10/day_10.txt', 'r') as file:
        data = parser(file)

    pt1, pt2 = solver(data)
    print(pt1)
    print(pt2)
