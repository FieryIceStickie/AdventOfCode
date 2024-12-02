from itertools import accumulate, pairwise
from math import comb
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO) -> list[list[int]]:
    return [[*map(int, line.split())] for line in raw_data.read().splitlines()]


# noinspection PyTypeChecker
def solver(data: list[list[int]]) -> tuple[int, int]:
    return tuple(
        sum(
            sum(v[0] * ((-1)**k if mode else comb(len(line), k)) for k, v in enumerate(
                accumulate([0] * (len(line) - 1), lambda seq, _: [j - i for i, j in pairwise(seq)], initial=line)))
            for line in data
        )
        for mode in (0, 1)
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        parsed_data = parser(file)

    print(*solver(parsed_data))
