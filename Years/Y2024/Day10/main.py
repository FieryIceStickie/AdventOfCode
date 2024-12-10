from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    zeroes = set()
    return {
        (z := x+1j*y): [v == '0' and zeroes.add(z)] and int(v)
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
    }, zeroes


def full_solver(data: dict[complex, int], zeroes: set[complex]):
    p1 = p2 = 0
    for start in zeroes:
        bfs = [start]
        nines = set()
        for z in bfs:
            if data[z] == 9:
                p2 += 1
                nines.add(z)
                continue
            for d in (-1, 1j, 1, -1j):
                loc = z + d
                if data.get(loc, None) == data[z] + 1:
                    bfs.append(loc)
        p1 += len(nines)
    return p1, p2


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(*data))
