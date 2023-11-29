from io import StringIO
from typing import TextIO

from Python.path_stuff import *
from Python.Tools.utils import facing_dict


def parser(raw_data: TextIO) -> list[list[complex]]:
    return [[*map(facing_dict['letters'].__getitem__, row)] for row in raw_data.read().splitlines()]


def part_a_solver(instructions: list[list[complex]]):
    res = StringIO()
    z = 1+1j
    for moves in instructions:
        for d in moves:
            z += d
            if not (0 <= z.real <= 2 and 0 <= z.imag <= 2):
                z -= d
        res.write(str(1 + int(3*z.real + z.imag)))
    return res.getvalue()


def part_b_solver(instructions: list[list[complex]]):
    locs = iter('123456789ABCD')
    loc_dict = {z: next(locs) for x in range(5) for y in range(5) if abs((z := x+1j*y) - (2+2j)) <= 2}
    res = StringIO()
    z = 2
    for moves in instructions:
        for d in moves:
            z += d
            if abs(z - (2+2j)) > 2:
                z -= d
        res.write(loc_dict[z])
    return res.getvalue()


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day2/day_2.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
