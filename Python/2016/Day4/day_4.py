from typing import TextIO
import re
from collections import Counter
from operator import itemgetter

from Python.path_stuff import *


pattern = re.compile(r'([a-z]+)(\d+)\[(\w{5})]')
other_pattern = re.compile(r'([a-z-]+)-(\d+).*')


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def verify(data: str) -> int:
    words, d, check = pattern.match(data.replace('-', '')).groups()
    c = sorted(Counter(words).items(), key=lambda x: (-x[1], x[0]))
    return int(d) if ''.join(map(itemgetter(0), c[:5])) == check else 0


def part_a_solver(data: list[str]):
    return sum(map(verify, data))


def part_b_solver(data: list[str]):
    real = (other_pattern.match(row).groups() for row in data if verify(row))
    trans = []
    base = mod = 'abcdefghijklmnopqrstuvwxyz'
    for _ in range(26):
        trans.append(str.maketrans(base + '-', mod + ' '))
        mod = mod[1:] + mod[0]
    return [(word.translate(trans[int(num) % 26]), int(num)) for word, num in real]


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 4/day_4.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    res = part_b_solver(data)
    for word, code in res:
        print(f'{code}: {word}')
