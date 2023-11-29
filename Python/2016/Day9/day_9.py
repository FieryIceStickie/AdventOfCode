import re
from math import prod
from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_solver(data: str):
    res = 0
    skip = 0
    for c in re.findall(r'\(\d+x\d+\)|\w', data):
        if skip:
            skip -= len(c)
            res += len(c) * r
            continue
        elif len(c) > 1:
            w, r = map(int, c[1:-1].split('x'))
            skip = w
        else:
            res += 1
    return res


def part_b_solver(data: str):
    res = 0
    active = []
    for c in re.findall(r'\(\d+x\d+\)|\w', data):
        l = len(c)
        if len(c) > 1:
            w, r = map(int, c[1:-1].split('x'))
            active.append((w+l, r))
            active = [(s-l, r) for s, r in active if s > l]
        else:
            res += prod(r for s, r in active)
            active = [(s-1, r) for s, r in active if s > 1]
    return res


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day9/day_9.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
