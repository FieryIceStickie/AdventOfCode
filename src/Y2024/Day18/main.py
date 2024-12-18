from typing import TextIO
import re
from collections import deque
from itertools import batched
from attrs import define

from Tools.Python.Utils.utils import reversed_enumerate
from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [x+1j*y for x, y in batched(map(int, re.findall(r'\d+', raw_data.read())), 2)]


def get_within(size: int):
    return lambda z: 0 <= z.real < size and 0 <= z.imag < size


def part_a_solver(data: list[complex], size: int):
    grid = set(data[:1024])
    within = get_within(size)
    active = deque([(0, 0)])
    visited = {0: 0}
    end = (size - 1) * (1 + 1j)
    while active:
        loc, cost = active.popleft()
        if loc == end:
            return cost
        neighbors = {
            (z, cost + 1)
            for d in (-1, -1j, 1j, 1)
            if (z := loc + d) not in visited
            if z not in grid
            if within(z)
        }
        active.extend(neighbors)
        visited |= neighbors


@define
class Node:
    parent: complex
    size: int = 1


class DSU[K, V](dict[K, V]):
    def find_set(self, z: K) -> K:
        if z == self[z].parent:
            return z
        res = self.find_set(self[z].parent)
        self[z].parent = res
        return res

    def union_set(self, z1: K, z2: K):
        a = self.find_set(z1)
        b = self.find_set(z2)
        if a != b:
            if self[a].size < self[b].size:
                a, b = b, a
            self[b].parent = a
            self[a].size += self[b].size


def part_b_solver(data: list[complex], size: int):
    sdata = set(data)
    end = (size - 1) * (1 + 1j)
    dsu = DSU({
        z: Node(z)
        for x in range(size)
        for y in range(size)
        if (z := x+1j*y) not in sdata
    })
    for z in dsu:
        for d in (1, 1j):
            if (loc := z + d) in dsu:
                dsu.union_set(loc, z)
    for t, z in reversed_enumerate(data):
        dsu[z] = Node(z)
        for d in (-1, 1j, 1, -1j):
            loc = z + d
            if loc in dsu:
                dsu.union_set(loc, z)
        if dsu.find_set(0) == dsu.find_set(end):
            return f'{int(z.real)},{int(z.imag)}'


if __name__ == '__main__':
    testing = False
    size = 7 if testing else 71
    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data, size))
    print(part_b_solver(data, size))
