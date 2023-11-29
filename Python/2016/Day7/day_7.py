import re
from itertools import chain
from typing import TextIO

from Python.path_stuff import *

abba_pattern = re.compile(r'\w*(?!(\w)\1{3})(\w)(\w)\3\2')
aba_pattern = re.compile(r'(?=((?!(\w)\2{2})(\w)\w\3))')


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data: list[str]):
    return sum(
        any(map(abba_pattern.match, s[::2])) and not any(map(abba_pattern.match, s[1::2]))
        for s in map(re.compile(r'[\[\]]').split, data)
    )


def part_b_solver(data: list[str]):
    return sum(
        bool(bab := [f'{b}{a}{b}' for (a, b, _), *_ in chain.from_iterable(map(aba_pattern.findall, s[::2]))])
        and any(any(i in m for m in s[1::2]) for i in bab)
        for s in map(re.compile(r'[\[\]]').split, data)
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day7/day_7.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
