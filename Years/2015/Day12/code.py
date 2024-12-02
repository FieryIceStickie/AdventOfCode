import json
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return json.loads(raw_data.read())


def part_a_solver(data: dict):
    if isinstance(data, list):
        return sum(map(part_a_solver, data))
    elif isinstance(data, dict):
        return sum(map(part_a_solver, data.values()))
    elif isinstance(data, int):
        return data
    elif isinstance(data, str):
        return 0


def part_b_solver(data: dict):
    if isinstance(data, list):
        return sum(map(part_b_solver, data))
    elif isinstance(data, dict):
        return 0 if 'red' in data.values() else sum(map(part_b_solver, data.values()))
    elif isinstance(data, int):
        return data
    elif isinstance(data, str):
        return 0


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
