import heapq
import math
from collections.abc import Iterable
from itertools import combinations
from typing import TextIO

from attrs import define

type Point = tuple[int, int, int]


@define
class Node:
    parent: int
    size: int = 1


type DSU = list[Node]


def parser(raw_data: TextIO) -> list[Point]:
    return [
        tuple(map(int, line.split(",")))  # pyright: ignore[reportReturnType]
        for line in raw_data.read().splitlines()
    ]


def find_set(dsu: DSU, x: int) -> int:
    if dsu[x].parent == x:
        return x
    dsu[x].parent = find_set(dsu, dsu[x].parent)
    return dsu[x].parent


def union(dsu: DSU, x: int, y: int) -> None:
    a = find_set(dsu, x)
    b = find_set(dsu, y)
    if a == b:
        return
    if dsu[a].size > dsu[b].size:
        a, b = b, a
    dsu[a].parent = b
    dsu[b].size += dsu[a].size


def k_smallest[T](it: Iterable[T], k: int) -> list[T]:
    heap: list[T] = []
    for elem in it:
        if len(heap) == k:
            _ = heapq.heappushpop(heap, elem)
        else:
            heapq.heappush(heap, elem)
    return heap


def full_solver(points: list[Point]) -> tuple[int, int]:
    (*dsu,) = map(Node, range(len(points)))
    pairs = [
        (math.dist(points[x], points[y]), x, y)
        for x, y in combinations(range(len(points)), 2)
    ]
    heapq.heapify(pairs)
    for _ in range(1000):
        _, x, y = heapq.heappop(pairs)
        union(dsu, x, y)
    sizes = (dsu[x].size for x in range(len(points)) if dsu[x].parent == x)
    p1 = math.prod(k_smallest(sizes, 3))

    while True:
        _, x, y = heapq.heappop(pairs)
        union(dsu, x, y)
        if dsu[find_set(dsu, x)].size == len(points):
            return p1, points[x][0] * points[y][0]


if __name__ == "__main__":
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = "input.txt"
    else:
        path = test_path if testing else "input.txt"

    with open(path, "r") as file:
        data = parser(file)

    print(*full_solver(data))
