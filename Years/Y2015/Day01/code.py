from itertools import accumulate
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_solver(instructions: str):
    return sum((-1)**(i == ')') for i in instructions)


def part_b_solver(instructions: str):
    return next(i for i, v in enumerate(accumulate((-1)**(i == ')') for i in instructions), start=1) if v == -1)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
