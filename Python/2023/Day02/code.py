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


def solver(games: list[list[Counter[str]]]) -> tuple[int, int]:
    threshold = Counter({'red': 12, 'green': 13, 'blue': 14})
    mega_bags = [reduce(or_, game) for game in games]
    return (
        sum(idx for idx, bag in enumerate(mega_bags, start=1) if bag <= threshold),
        sum(prod(bag.values()) for bag in mega_bags),
            )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(data))
