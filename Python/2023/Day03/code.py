from itertools import groupby
from math import prod
from typing import TextIO

from Python.path_stuff import *
from Python.Tools.utils import all_deltas


def parser(raw_data: TextIO) -> tuple[dict[complex, complex], dict[complex, str]]:
    loc_dict = {}
    symbols = {}
    c = 0
    for x, row in enumerate(raw_data.read().splitlines()):
        y = 0
        for k, (*g,) in groupby(row, key=lambda c: c.isdigit() or c):
            if g[0] == '.':
                y += len(g)
                continue
            elif g[0].isdigit():
                num = int(''.join(g))
                for _ in range(len(g)):
                    loc_dict[x + 1j*y] = num + 1j*c
                    y += 1
                c += 1
            else:
                if len(g) != 1:
                    raise ValueError('Adjacent symbols found, pls send help')
                symbols[x + 1j*y] = g[0]
                y += 1
    return loc_dict, symbols


def part_a_solver(loc_dict: dict[complex, complex], symbols: dict[complex, str]):
    return sum(
        int(z.real) for z in {
            loc_dict[s+d]
            for s in symbols
            for d in all_deltas
            if s+d in loc_dict
        }
    )


def part_b_solver(loc_dict: dict[complex, complex], symbols: dict[complex, str]):
    return sum(
        int(prod(z.real for z in gears))
        for s in symbols
        if len(gears := {loc_dict[s+d] for d in all_deltas if s+d in loc_dict}) == 2
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        a, b = parser(file)

    print(part_a_solver(a.copy(), b.copy()))
    print(part_b_solver(a, b))
