import re
from typing import TextIO

import numpy as np

from Python.path_stuff import *


def parser(raw_data: TextIO):
    pattern = re.compile(r'(rect|rotate (?:row|column)) (?:[xy]=)?(\d+)(?:x| by )(\d+)')
    return [(a, int(b), int(c)) for a, b, c in (pattern.match(row).groups() for row in raw_data.read().splitlines())]


def do_instructions(data: list[tuple[str, int, int]]):
    screen = np.zeros((6, 50), dtype=bool)
    for row in data:
        match row:
            case 'rect', width, height:
                screen[:height, :width] = 1
            case 'rotate row', row, shift:
                screen[row, :] = np.roll(screen[row, :], shift)
            case 'rotate column', col, shift:
                screen[:, col] = np.roll(screen[:, col], shift)
    return screen


def part_a_solver(screen: np.ndarray):
    return np.count_nonzero(screen)


def part_b_solver(screen: np.ndarray):
    return '\n'.join(''.join(' █'[bool(v)] for v in row) for row in screen)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    screen = do_instructions(data)
    print(part_a_solver(screen))
    print(part_b_solver(screen))
