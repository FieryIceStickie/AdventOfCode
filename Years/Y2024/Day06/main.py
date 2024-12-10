from typing import TextIO
from collections import defaultdict

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return {
        x+1j*y: (guard := x+1j*y) and False if v == '^' else v == '#'
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
    }, guard


def full_solver(grid: dict[complex, bool], guard: complex):
    visited = defaultdict(set)
    phantom_visited = defaultdict(set)
    active_block = None
    blocks = set()
    eset = set()
    active = [(False, guard, -1)]
    while active:
        is_phantom, loc, d = active.pop()
        if (z := loc + d) not in grid:
            if is_phantom:
                phantom_visited.clear()
        elif grid[z] or z == active_block and rotate < 3:
            active.append((is_phantom, loc, d / 1j))
            rotate += 1
            continue
        elif d in visited.get(z, eset) or d in phantom_visited.get(z, eset):
            blocks.add(active_block)
            phantom_visited.clear()
        else:
            active.append((is_phantom, z, d))
            if not is_phantom and z not in visited:
                active.append((True, loc, d / 1j))
                active_block = z
            [visited, phantom_visited][is_phantom][z].add(d)
        rotate = 0
    return len(visited), len(blocks)


if __name__ == '__main__':
    testing = True

    with open('test.txt' if testing else 'input.txt', 'r') as file:
        data = parser(file)
    print(*full_solver(*data))
