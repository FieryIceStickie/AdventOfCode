from collections import defaultdict
from typing import TextIO

from Python.path_stuff import *
from Python.Tools.utils import deltas


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


def solver(loc_dict: dict[complex, tuple[int, complex]], row_len: int, col_len: int) -> tuple[int, int]:
    def sim(start: tuple[complex, complex]):
        visited = defaultdict(set)
        active = [start]
        while active:
            loc, facing = active.pop()
            if facing in visited.get(loc, ()):
                continue
            if not (row_len > loc.real >= 0 <= loc.imag < col_len):
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

    return sim((0, 1j)), max(
        sim((z, facing))
        for facing, locs in zip(
            deltas,
            [
                [complex(row_len - 1, i) for i in range(col_len)],
                [complex(i, 0) for i in range(row_len)],
                [complex(0, i) for i in range(col_len)],
                [complex(i, col_len - 1) for i in range(row_len)],
            ]
        )
        for z in locs
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(*data))
