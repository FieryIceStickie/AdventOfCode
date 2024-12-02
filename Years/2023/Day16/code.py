import multiprocessing
from collections import defaultdict
from functools import partial
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    parse_dict = {
        '/': (0, 1j),
        '\\': (0, -1j),
        '-': (1, 1),
        '|': (1, 1j),
    }
    grid_data = raw_data.read().splitlines()
    return {
        x + 1j * y: parse_dict[v]
        for x, row in enumerate(grid_data)
        for y, v in enumerate(row)
        if v != '.'
    }, len(grid_data), len(grid_data[0])


def sim(loc_dict: dict[complex, tuple[int, complex]],
        row_len: int, col_len: int,
        start: tuple[complex, complex]) -> int:
    visited = defaultdict(set)
    active = [start]
    while active:
        loc, facing = active.pop()
        if not (row_len > loc.real >= 0 <= loc.imag < col_len):
            continue
        if facing in visited[loc]:
            continue
        visited[loc].add(facing)
        if loc in loc_dict:
            tile_type, tile_value = loc_dict[loc]
            if not tile_type:
                new_facing = (facing * tile_value).conjugate()
                active.append((loc + new_facing, new_facing))
                continue
            elif not (facing * tile_value).imag:
                for d in (1j, -1j):
                    new_facing = facing * d
                    active.append((loc + new_facing, new_facing))
                continue
        active.append((loc + facing, facing))
    return len(visited)

def solver(loc_dict: dict[complex, tuple[int, complex]], row_len: int, col_len: int) -> tuple[int, int]:
    filled_sim = partial(sim, loc_dict, row_len, col_len)
    with multiprocessing.Pool() as pool:
        return filled_sim((0, 1j)), max(pool.imap_unordered(
            filled_sim,
            [
                *[(complex(row_len - 1, i), -1) for i in range(col_len)],
                *[(complex(i, 0), 1j) for i in range(row_len)],
                *[(complex(0, i), 1) for i in range(col_len)],
                *[(complex(i, col_len - 1), -1j) for i in range(row_len)],
            ],
            chunksize=4,
        ))

if __name__ == '__main__':
    def main():
        testing = False

        with open(test_path if testing else 'input.txt', 'r') as file:
            data = parser(file)

        print(*solver(*data))
    import timeit
    print(timeit.timeit(main, number=1))