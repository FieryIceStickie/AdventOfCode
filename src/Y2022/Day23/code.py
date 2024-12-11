from collections import defaultdict, deque
from itertools import count

from src.Tools.utils import display_visited


def parser(filename: str):
    with open(filename, 'r') as file:
        return {x+y*1j for x, row in enumerate(file.read().splitlines()) for y, v in enumerate(row) if v == '#'}


class FinishMovement(Exception):
    pass


def sim(elf_set: set[complex], directions: deque[tuple[complex, ...]], surroundings: set[complex, ...]):
    proposals = defaultdict(list)
    for z in {z for z in elf_set if any(z + d in elf_set for d in surroundings)}:
        for d in directions:
            if all(z + dz not in elf_set for dz in d):
                proposals[z + d[1]].append(z)
                break

    moved = False

    for z, elves in proposals.items():
        if len(elves) == 1:
            elf_set -= {elves[0]}
            elf_set |= {z}
            moved = True
    if not moved:
        raise FinishMovement
    directions.rotate(-1)


def part_a_solver(elf_set: set[complex]):
    directions = deque([(-1 - 1j, -1, -1 + 1j), (1 - 1j, 1, 1 + 1j), (-1 - 1j, -1j, 1 - 1j), (-1 + 1j, 1j, 1 + 1j)])
    surroundings = {-1 - 1j, -1, -1 + 1j, 1j, 1 + 1j, 1, 1 - 1j, -1j}
    for _ in range(10):
        sim(elf_set, directions, surroundings)
    reals, imags = {z.real for z in elf_set}, {z.imag for z in elf_set}
    row_min, row_max, col_min, col_max = min(reals), max(reals), min(imags), max(imags)
    return int((row_max-row_min+1)*(col_max-col_min+1)- len(elf_set))


def part_b_solver(elf_set: set[complex]):
    directions = deque([(-1 - 1j, -1, -1 + 1j), (1 - 1j, 1, 1 + 1j), (-1 - 1j, -1j, 1 - 1j), (-1 + 1j, 1j, 1 + 1j)])
    surroundings = {-1 - 1j, -1, -1 + 1j, 1j, 1 + 1j, 1, 1 - 1j, -1j}
    i = 0
    try:
        for i in count(1):
            sim(elf_set, directions, surroundings)
    except FinishMovement:
        return i


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs.copy()))
    print(part_b_solver(inputs))
