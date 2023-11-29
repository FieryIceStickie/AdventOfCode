from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver():
    return


def part_b_solver():
    return 


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2020/Day 17/day_17.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
