from typing import TextIO
from collections import deque
from itertools import count

from Python.path_stuff import *



def parser(raw_data: TextIO):
    return int(raw_data.read())


def part_a_solver(offset: int):
    def is_wall(z: complex) -> bool:
        x, y = z.real, z.imag
        num = int(x*x + 3*x + 2*x*y + y + y*y + offset)
        return num.bit_count() & 1
    paths = {}
    active = deque([1+1j])
    visited = {1+1j}
    while active:
        current = active.popleft()
        if current == 31+39j:
            break
        for d in (-1, 1j, 1, -1j):
            node = current + d
            if node in visited:
                continue
            visited.add(node)
            if not is_wall(node) and node.real >= 0 <= node.imag:
                active.append(node)
                paths[node] = current
    for i in count(1):
        current = paths[current]
        if current == 1+1j:
            break
    return i


def part_b_solver(offset: int):
    def is_wall(z: complex) -> bool:
        x, y = z.real, z.imag
        num = int(x*x + 3*x + 2*x*y + y + y*y + offset)
        return num.bit_count() & 1

    active = deque([(1+1j, 0)])
    visited = {1+1j}
    locs = {1+1j}
    while active:
        current, steps = active.popleft()
        if steps == 50:
            continue
        for d in (-1, 1j, 1, -1j):
            node = current + d
            if node.real < 0 or node.imag < 0:
                continue
            if node in visited:
                continue
            visited.add(node)
            if not is_wall(node):
                active.append((node, steps+1))
                locs.add(node)
    return len(locs)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 13/day_13.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
