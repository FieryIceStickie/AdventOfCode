import re
from collections import Counter
from functools import reduce
from math import prod
from operator import or_
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO) -> list[Counter[str]]:
    return [reduce(or_, [Counter({color: int(num)})
                         for num, color in re.findall(r'(\d+) (\w+)', line)])
            for line in raw_data.read().splitlines()]


def solver(games: list[Counter[str]]) -> tuple[int, int]:
    threshold = Counter({'red': 12, 'green': 13, 'blue': 14})
    return (
        sum(idx for idx, bag in enumerate(games, start=1) if bag <= threshold),
        sum(prod(bag.values()) for bag in games),
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(data))
