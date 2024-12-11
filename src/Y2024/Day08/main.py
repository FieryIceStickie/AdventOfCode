from collections import defaultdict
from itertools import combinations, count
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    antennas = defaultdict(set)
    for x, row in enumerate(raw_data.read().splitlines()):
        for y, v in enumerate(row):
            if v != '.':
                antennas[v].add(x+1j*y)
    return antennas, x + 1, y + 1


def full_solver(antennas: dict[str, set[complex]], height: int, width: int):

    def within(z: complex) -> bool:
        return 0 <= z.real < height and 0 <= z.imag < width

    p1_antinodes = set()
    p2_antinodes = set()
    for antenna, locs in antennas.items():
        for z1, z2 in combinations(locs, 2):
            d = z2 - z1
            if within(z2 + d):
                p1_antinodes.add(z2 + d)
            if within(z1 - d):
                p1_antinodes.add(z1 - d)
            while within(z2):
                p2_antinodes.add(z2)
                z2 += d
            while within(z1):
                p2_antinodes.add(z1)
                z1 -= d
    return len(p1_antinodes), len(p2_antinodes)


if __name__ == '__main__':
    testing = False
    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(*data))