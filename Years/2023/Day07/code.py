from operator import itemgetter
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    table = str.maketrans('TJQKA', 'abcde')
    return [(hand.translate(table), int(bid)) for hand, bid in map(str.split, raw_data.read().splitlines())]


def part_a_solver(data: list[tuple[str, int]]):
    return sum(i*j for i, j in enumerate(
        map(itemgetter(1), sorted(data, key=lambda s: (sum(map(s[0].count, s[0])), s[0]))),
        start=1,
    ))


def part_b_solver(data):
    return sum(i*j for i, j in enumerate(
        map(itemgetter(1), sorted(
            [(hand.replace('b', '1'), bid) for hand, bid in data],
            key=lambda s: (max(sum(map(s[0].replace('1', j).count, s[0].replace('1', j))) for j in s[0]), s[0])
        )),
        start=1,
    ))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
