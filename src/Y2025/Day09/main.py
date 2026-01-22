import time
from collections import deque
from itertools import (
    chain,
    combinations,
    islice,
    product,
    starmap,
)
from typing import TextIO

from attrs import frozen
from rich.pretty import pprint

type Point = tuple[int, int]


@frozen
class Floor:
    x: int
    y_left: int
    y_right: int


@frozen
class Wall:
    y: int
    x_left: int
    x_right: int


type Edge = Floor | Wall


def to_edge(p1: Point, p2: Point) -> Edge:
    if p1[0] == p2[0]:
        left, right = sorted([p1[1], p2[1]])
        return Floor(p1[0], left, right)
    elif p1[1] == p2[1]:
        left, right = sorted([p1[0], p2[0]])
        return Wall(p1[1], left, right)
    else:
        raise ValueError("Edge is cooked bro")


def parser(raw_data: TextIO) -> list[Point]:
    return [
        tuple(map(int, line.split(",")))  # pyright: ignore[reportReturnType]
        for line in raw_data.read().splitlines()
    ]


def compress(values: set[int]) -> tuple[dict[int, int], int]:
    return {v: 2 * i for i, v in enumerate(sorted(values))}, 2 * len(values) - 1


def full_solver(points: list[Point]) -> tuple[int, int]:
    x_values, x_len = compress({x for x, _ in points})
    y_values, y_len = compress({y for _, y in points})
    boundary: set[Point] = set()
    for edge in starmap(
        to_edge, zip(points, chain(islice(points, 1, None), [points[0]]))
    ):
        match edge:
            case Floor(x, y_left, y_right):
                boundary |= {
                    (x_values[x], y)
                    for y in range(y_values[y_left], y_values[y_right] + 1)
                }
            case Wall(y, x_left, x_right):
                boundary |= {
                    (x, y_values[y])
                    for x in range(x_values[x_left], x_values[x_right] + 1)
                }

    sides = chain(
        ((0, y) for y in range(y_len)),
        ((x, y_len - 1) for x in range(1, x_len - 1)),
        ((x_len - 1, y) for y in range(y_len)),
        ((x, 0) for x in range(1, x_len - 1)),
    )
    active = deque([point for point in sides if point not in boundary])
    outer = {*active}
    previsited = boundary | outer
    visited: set[Point] = set()
    while active:
        x, y = active.popleft()
        for p in [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]:
            if p in previsited or p in visited:
                continue
            zx, zy = p
            if not (0 <= zx < x_len and 0 <= zy <= y_len):
                continue
            active.append(p)
            visited.add(p)
    visited |= outer

    dp = [[0 for _ in range(y_len)] for _ in range(x_len)]
    for x, y in product(range(x_len), range(y_len)):
        res = (x, y) in visited
        if x > 0 and y > 0:
            res -= dp[x - 1][y - 1]
        if x > 0:
            res += dp[x - 1][y]
        if y > 0:
            res += dp[x][y - 1]
        dp[x][y] = res

    p1 = p2 = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        area = (abs(y2 - y1) + 1) * (abs(x2 - x1) + 1)
        p1 = max(p1, area)
        if area < p2:
            continue
        u1, u2 = sorted([x_values[x1], x_values[x2]])
        v1, v2 = sorted([y_values[y1], y_values[y2]])
        num_nones = dp[u2][v2]
        if u1 > 0 and v1 > 0:
            num_nones += dp[u1 - 1][v1 - 1]
        if u1 > 0:
            num_nones -= dp[u1 - 1][v2]
        if v1 > 0:
            num_nones -= dp[u2][v1 - 1]
        if not num_nones:
            p2 = area

    return p1, p2


if __name__ == "__main__":
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = "input.txt"
    else:
        path = test_path if testing else "input.txt"

    st = time.perf_counter()
    with open(path, "r") as file:
        data = parser(file)

    pprint(full_solver(data))
    ed = time.perf_counter()
    print(ed - st)
