from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return sorted(((*map(int, row.split('-')),) for row in raw_data.read().splitlines()))


def part_a_solver(data: list[tuple[int, int]]):
    current = 0
    for start, end in data:
        if start > current + 1:
            return current + 1
        current = max(end, current)

def part_b_solver(data: list[tuple[int, int]]):
    count = 0
    current = 0
    for start, end in data:
        if start > current + 1:
            count += start - current - 1
        current = max(end, current)
    return count + max(4294967295 - current, 0)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
