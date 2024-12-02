from bisect import insort
from itertools import groupby, pairwise
from operator import itemgetter
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO) -> tuple[list[int], list[int]]:
    imags = []
    reals = [
        insort(imags, y) or x
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
        if v == '#'
    ]
    return reals, imags


def solver(reals: list[int], imags: list[int]) -> tuple[int, ...]:
    n = len(reals)
    return tuple(
        sum(
            i * (n-i) * ((p2 - p1 - 1)*size + 1)
            for nums in (reals, imags)
            for (p1, _), (p2, ((i, _), *_)) in pairwise(groupby(enumerate(nums), key=itemgetter(1)))
        )
        for size in (2, 1000000)
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(*data))
