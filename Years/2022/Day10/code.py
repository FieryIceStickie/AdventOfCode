from itertools import accumulate

import numpy as np


def parser(filename: str):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def part_a_solver(instructions: list[str]):
    cycles = [1 if i == 'noop' else 2 for i in instructions]
    adds = [0 if not i[5:] else int(i[5:]) for i in instructions]
    cum_cycles = np.array([*accumulate(cycles)])
    cum_adds = np.array([*accumulate(adds)]) + 1
    idxs = np.searchsorted(cum_cycles, np.arange(20, 221, 40)) - 1
    return sum(cum_adds[idxs] * np.arange(20, 221, 40))


def part_b_solver(instructions: list[str]):
    cycles = [1 if i == 'noop' else 2 for i in instructions]
    adds = [0 if not i[5:] else int(i[5:]) for i in instructions]
    cum_cycles = np.array([*accumulate(cycles)])
    cum_adds = np.array([*accumulate(adds)]) + 1

    screen = np.zeros((6, 40))
    sprite_pos = 1
    i = 0
    for (r, c), _ in np.ndenumerate(screen):
        cycle = 40 * r + c
        if cycle in cum_cycles:
            sprite_pos = cum_adds[i]
            i += 1
        if abs(c - sprite_pos) <= 1:
            screen[(r, c)] = 1
    return '\n'.join(''.join('█' if i else '.' for i in row) for row in screen)


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
