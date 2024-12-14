from operator import itemgetter
from typing import TextIO
import re
from itertools import batched
from collections import Counter

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [*batched(map(int, re.findall(r'-?\d+', raw_data.read())), 4)]


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
