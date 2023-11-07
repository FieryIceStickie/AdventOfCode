from typing import TextIO

from path_stuff import *


def parser(raw_data: TextIO):
    data = raw_data.read()
    return int(data.translate(str.maketrans('.^', '01')), 2), len(data)


def solve(row: int, size: int, iterations: int):
    mask = (1 << size) - 1
    res = row.bit_count()
    for _ in range(iterations - 1):
        row = (row << 1 ^ row >> 1) & mask
        res += row.bit_count()
    return size * iterations - res


def part_a_solver(row: int, size: int):
    return solve(row, size, 40)


def part_b_solver(row: int, size: int):
    return solve(row, size, 400000)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 18/day_18.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(*data))
    print(part_b_solver(*data))
