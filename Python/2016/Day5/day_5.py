from typing import TextIO
import hashlib
from itertools import count, islice
from operator import itemgetter

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_solver(secret_key: str):
    return ''.join(islice((h[5] for i in count(0) if (h := hashlib.md5(f'{secret_key}{i}'.encode()).hexdigest())[:5] == '00000'), None, 8))


def part_b_solver(secret_key: str):
    seen = set()
    return ''.join(map(itemgetter(1), sorted(islice(((seen.add(h[5]) or h[5:7] for i in count(0) if (h := hashlib.md5(f'{secret_key}{i}'.encode()).hexdigest())[:5] == '00000' and h[5] not in seen and h[5] in '01234567')), None, 8))))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 5/day_5.txt', 'r') as file:
        data = parser(file)

    # print(part_a_solver(data))
    print(part_b_solver(data))
