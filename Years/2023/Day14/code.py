from itertools import count, islice
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO) -> tuple[frozenset[complex], frozenset[complex], int, int]:
    rocks = set()
    walls = set()
    for x, row in enumerate(raw_data.read().splitlines()):
        for y, v in enumerate(row):
            loc = x + 1j * y
            if v == '#':
                walls.add(loc)
            elif v == 'O':
                rocks.add(loc)
    return frozenset(rocks), frozenset(walls), x + 1, y + 1


def solver(curr_rocks: frozenset[complex], walls: frozenset[complex], row_len: int, col_len: int) -> tuple[int, int]:
    facing_ranges = {
        -1: ([complex(row_len - 1, i) for i in range(col_len)[::-1]], complex(-1, col_len - 1)),
        1j: ([complex(i, 0) for i in range(row_len)[::-1]], complex(row_len - 1, col_len)),
        1: ([complex(0, i) for i in range(col_len)], complex(row_len, 0)),
        -1j: ([complex(i, col_len - 1) for i in range(row_len)], complex(0, -1)),
    }

    p1_rtn: int | None = None

    def sim(rocks: frozenset[complex], facing: complex) -> frozenset[complex]:
        nonlocal p1_rtn
        rtn = set()
        starts, end = facing_ranges[facing]
        for z in starts:
            cumulant = 0
            while z != end:
                if z in rocks:
                    cumulant += 1
                elif z in walls:
                    back_vec = z
                    for _ in range(cumulant):
                        back_vec -= facing
                        rtn.add(back_vec)
                    cumulant = 0
                z += facing
            for _ in range(cumulant):
                z -= facing
                rtn.add(z)
            end += 1j * facing
        p1_rtn = p1_rtn or sum(int(row_len - z.real) for z in rtn)
        return frozenset(rtn)

    def sim_cycle(rocks: frozenset[complex]):
        for d in (-1, -1j, 1, 1j):
            rocks = sim(rocks, d)
        return rocks

    cache = {curr_rocks: 0}
    for step in count(1):
        curr_rocks = sim_cycle(curr_rocks)
        if curr_rocks in cache:
            break
        cache[curr_rocks] = step
    starting_offset = cache[curr_rocks]
    cycle_len = step - starting_offset
    return p1_rtn, sum(int(row_len - z.real)
                       for z in next(islice(cache, starting_offset + (1_000_000_000 - starting_offset) % cycle_len)))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(*data))
