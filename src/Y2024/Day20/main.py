from typing import TextIO

from numpy.random.mtrand import Sequence

from Tools.Python.path_stuff import *
# from Tools.Python.utils.utils import close_enumerate


def parser(raw_data: TextIO):
    grid = set()
    for x, row in enumerate(raw_data.read().splitlines()):
        for y, v in enumerate(row):
            z = x + 1j * y
            if v == "S":
                start = z
            elif v == 'E':
                end = z
            elif v == '#':
                grid.add(z)
    return grid, start, end


def manhattan(z: complex) -> int:
    return int(abs(z.real)) + int(abs(z.imag))


def full_solver(grid: set[complex], start: complex, end: complex):
    path = [start]
    costs = {start: 0}
    for cost, z in enumerate(path):
        costs[z] = cost
        if z == end:
            break
        loc = next(
            loc for d in (-1, 1j, 1, -1j)
            if (loc := z + d) not in grid
            and loc not in costs
        )
        path.append(loc)
    p1 = sum(
        abs(costs.get(z + d, cost) - cost) >= 102
        for z, cost in costs.items()
        for d in (2, 1 - 1j, -2j, -1 - 1j)
    )
    p2 = sum(
        c2 - c1 - dist >= 100
        for c1, z1 in enumerate(path)
        for c2, dist in close_enumerate(path, z1, c1 + 102)
    )
    return p1, p2


def close_enumerate(path: Sequence[complex], target: complex, start: int):
    idx = start
    while idx < len(path):
        v = path[idx]
        dist = manhattan(v - target)
        if dist > 20:
            idx += dist - 20
        else:
            yield idx, dist
            idx += 1


if __name__ == '__main__':
    testing = False
    import time
    st = time.perf_counter()
    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    print(*full_solver(*data))
    ed = time.perf_counter()
    print(ed - st)
