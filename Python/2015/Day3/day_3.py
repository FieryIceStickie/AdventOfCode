from typing import TextIO

from Python.path_stuff import *
from Python.Tools.utils import facing_dict


def parser(raw_data: TextIO):
    return [*map(facing_dict['arrows'].__getitem__, raw_data.read())]


def part_a_solver(directions: list[complex]):
    z = 0
    visited = {z}
    for d in directions:
        z += d
        visited |= {z}
    return len(visited)


def part_b_solver(directions: list[complex]):
    z, r = 0, 0
    visited = {0}
    for dz, dr in zip(*[iter(directions)]*2):
        z += dz
        r += dr
        visited |= {z, r}
    return len(visited)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day3/day_3.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
