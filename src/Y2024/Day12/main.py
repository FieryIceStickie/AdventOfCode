from typing import TextIO
from attrs import define

from Tools.Python.path_stuff import *


@define
class Region:
    parent: complex
    plant: str
    edges: set[tuple[complex, complex]] = None
    size: int = 1

    def __attrs_post_init__(self):
        self.edges = {
            (edge, self.parent + d)
            for edge, d in [(1j, 0), (1j, 1), (1, 0), (1, 1j)]
        }


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
            self[a].edges ^= self[b].edges


def parser(raw_data: TextIO):
    return DSU({
        (z := x+1j*y): Region(z, v)
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
    })


def full_solver(dsu: DSU[complex, Region]):
    for z in dsu:
        for d in (1j, 1):
            loc = z + d
            if loc in dsu and dsu[loc].plant == dsu[z].plant:
                dsu.union_set(z, loc)
    regions = set(map(dsu.find_set, dsu))
    p1 = sum(
        dsu[z].size * len(dsu[z].edges)
        for z in regions
    )
    p2 = sum(
        dsu[z].size * sum(
            1
            for edge, pos in dsu[z].edges
            if (edge, pos - edge) not in dsu[z].edges
            or {
                (alt_edge := 1+1j - edge, pos),
                (alt_edge, pos - alt_edge)
            }.issubset(dsu[z].edges)
        )
        for z in regions
    )
    return p1, p2


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(data))
