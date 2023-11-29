from typing import TextIO
import hashlib
from itertools import count

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_solver(secret_key: str):
    return next(i for i in count(0) if hashlib.md5(f'{secret_key}{i}'.encode()).hexdigest()[:5] == '00000')


def part_b_solver(secret_key: str):
    return next(i for i in count(0) if hashlib.md5(f'{secret_key}{i}'.encode()).hexdigest()[:6] == '000000')


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day4/day_4.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
