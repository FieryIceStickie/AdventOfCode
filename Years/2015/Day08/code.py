import ast
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data: list[str]):
    return sum(len(s) - len(ast.literal_eval(s)) for s in data)


def part_b_solver(data: list[str]):
    return sum(2 + s.count('\\') + s.count('"') for s in data)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
