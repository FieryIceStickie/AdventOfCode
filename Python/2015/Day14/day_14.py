from typing import TextIO

from Python.path_stuff import *
import re
from itertools import starmap
from functools import partial


def parser(raw_data: TextIO):
    return [[int(i) for i in re.findall(r'\d+', row)] for row in raw_data.read().splitlines()]


def dist(t: int, v: int, ft: int, rt: int):
    q, r = divmod(t, rt+ft)
    return ft*v*q + min(ft, r)*v


def part_a_solver(data: list[list[int]]):
    return max(starmap(partial(dist, 2503), data))


def part_b_solver(data: list[list[int]]):
    scores = [0] * len(data)
    locs = [0] * len(data)
    cooldowns = [ft for _, ft, _ in data]
    running = [True] * len(data)
    for _ in range(2503):
        for i, (cooldown, run) in enumerate(zip(cooldowns, running)):
            if not cooldown:
                running[i] = not run
                cooldowns[i] = data[i][1 + run] - 1
            else:
                cooldowns[i] -= 1
            if running[i]:
                locs[i] += data[i][0]
        top = max(locs)
        for i, v in enumerate(locs):
            if v == top:
                scores[i] += 1
    return max(scores)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day 14/day_14.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
