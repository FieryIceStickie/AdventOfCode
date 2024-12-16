from operator import itemgetter
from typing import TextIO
import re
from itertools import batched
from collections import Counter

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [*batched(map(int, re.findall(r'-?\d+', raw_data.read())), 4)]


"""
def part_a_solver(data):
    grid = np.zeros((h, w), dtype=int)
    for px, py, vx, vy in data:
        x, y = sim(px, py, vx, vy, 100)
        grid[y, x] += 1
    w2, h2 = w // 2, h // 2
    return prod(
        np.sum(a) for a in [grid[:h2, :w2], grid[h2+1:, :w2], grid[:h2, w2+1:], grid[h2+1:, w2+1:]]
    )


def sim(px, py, vx, vy, n):
    return (px + vx * n) % w, (py + vy * n) % h


def part_b_solver(data):
    tree = {
        m+1j*d
        for d in range(4)
        for m in range(-d, d+1)
    } | {-2+4j, -1+4j, 1+4j, 2+4j}
    for s in count(0):
        grid = {
            complex(*sim(px, py, vx, vy, s))
            for px, py, vx, vy in data
        }
        if any(
            z for z in grid
            if {z+d for d in tree}.issubset(grid)
        ):
            display_visited(grid)
            return s
"""


def full_solver(grid: list[tuple[int, int, int, int]], w: int, h: int):
    grid = [[px, vx, py, vy] for px, py, vx, vy in grid]
    xt = yt = 0
    p1 = None
    [(_, x_max)] = Counter(map(itemgetter(0), grid)).most_common(1)
    [(_, y_max)] = Counter(map(itemgetter(2), grid)).most_common(1)
    for t in range(1, max(w, h, 101)):
        for bot in grid:
            px, vx, py, vy = bot
            bot[0] = (px + vx) % w
            bot[2] = (py + vy) % h
        if t == 100:
            c = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            wh, hh = w // 2, h // 2
            for px, vx, py, vy in grid:
                c[(px < wh) - (px > wh)][(py < hh) - (py > hh)] += 1
            p1 = c[1][1] * c[1][2] * c[2][1] * c[2][2]
        [(_, mx)] = Counter(map(itemgetter(0), grid)).most_common(1)
        if mx > x_max:
            x_max = mx
            xt = t
        [(_, my)] = Counter(map(itemgetter(2), grid)).most_common(1)
        if my > y_max:
            y_max = my
            yt = t
    xt %= w
    yt %= h
    p2 = xt + (yt - xt) * pow(w, -1, h) * w % (w * h)
    return p1, p2


def disp_room(grid: list[tuple[int, int, int, int]], t: int, w: int, h: int) -> str:
    block = '██'
    space = '  '
    s = {
        ((px + vx * t) % w, (py + vy * t) % h)
        for px, py, vx, vy in grid
    }
    return '\n'.join(
        ''.join(
            block if (x, y) in s else space
            for x in range(w)
        )
        for y in range(h)
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    w, h = (11, 7) if testing else (101, 103)

    p1, p2 = full_solver(data, w, h)
    print(disp_room(data, p2, w, h))
    print(p1, p2)
