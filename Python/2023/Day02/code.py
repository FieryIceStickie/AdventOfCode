import re
from collections import Counter
from functools import reduce
from math import prod
from operator import or_
from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO) -> list[list[Counter[str]]]:
    return [[Counter({color: int(num) for num, color in bag})
             for bag in map(re.compile(r'(\d+) (red|green|blue)').findall,
                            line.split(';'))]
            for line in raw_data.read().splitlines()]


def part_a_solver(games: list[list[Counter[str]]]) -> int:
    threshold = Counter({'red': 12, 'green': 13, 'blue': 14})
    return sum(
        idx
        for idx, bags in enumerate(games, start=1)
        if all(bag <= threshold for bag in bags)
    )


def part_b_solver(games: list[list[Counter[str]]]) -> int:
    return sum(prod(reduce(or_, game).values()) for game in games)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
