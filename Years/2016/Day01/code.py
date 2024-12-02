from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO) -> list[tuple[complex, int]]:
    return [(-1j if s == 'L' else 1j, int(''.join(d))) for s, *d in raw_data.read().split(', ')]


def part_a_solver(steps: list[tuple[complex, int]]):
    loc = 0
    facing = -1
    for s, d in steps:
        facing *= s
        loc += facing * d
    return int(abs(loc.real) + abs(loc.imag))


def part_b_solver(steps: list[tuple[complex, int]]):
    loc = 0
    facing = -1
    visited = {0}
    for s, d in steps:
        facing /= s
        for _ in range(d):
            loc += facing
            if loc in visited:
                return int(abs(loc.real) + abs(loc.imag))
            visited.add(loc)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
