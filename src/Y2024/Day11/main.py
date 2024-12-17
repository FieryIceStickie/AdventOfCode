from typing import TextIO
from functools import cache
from itertools import repeat

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [*map(int, raw_data.read().split())]


@cache
def blink(num: int, n: int) -> int:
    if n == 0:
        return 1
    if num == 0:
        return blink(1, n - 1)
    string = str(num)
    l = len(string)
    if not l % 2:
        return blink(int(string[:l//2]), n - 1) + blink(int(string[l//2:]), n - 1)
    return blink(num * 2024, n - 1)


def part_a_solver(data: list[int]):
    return sum(map(blink, data, repeat(25)))


def part_b_solver(data: list[int]):
    return sum(map(blink, data, repeat(75)))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    print(part_a_solver(data))
    print(part_b_solver(data))
