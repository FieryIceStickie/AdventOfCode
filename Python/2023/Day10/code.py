from typing import TextIO

from Python.path_stuff import *
from Python.Tools.utils import deltas


def parser(raw_data: TextIO) -> dict[complex, str]:
    return {
        x + 1j*y: v
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
        if v != '.'
    }


def solver(loc_dict: dict[complex, str]) -> tuple[int, int]:
    start = next(z for z, v in loc_dict.items() if v == 'S')
    d = next(d for d, p in zip(deltas, '7|F J-7 L|J F-L'.split()) if loc_dict[start+d] in p)
    loc_mapping = {'L': -1+1j, 'J': -1-1j, 'F': 1+1j, '7': 1-1j, '|': 0, '-': 0}
    dfs = [start]
    for node in dfs:
        z = node + d
        if z == start:
            break
        dfs.append(z)
        d += loc_mapping[loc_dict[z]]
    area = abs(sum((z1 * z2.conjugate()).imag for z1, z2 in zip(dfs, dfs[1:] + dfs[:1])))
    return len(dfs) // 2, int(area - len(dfs) + 2) // 2


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(data))
