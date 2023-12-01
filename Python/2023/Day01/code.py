from typing import TextIO
import re

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data: list[str]):
    return sum(int(f'{nums[0]}{nums[-1]}') for nums in map(re.compile(r'\d').findall, data))


def part_b_solver(data: list[str]):
    nums = 'zero|one|two|three|four|five|six|seven|eight|nine'
    new_data = [
        re.sub(
            fr'(?=({nums}))',
            lambda s: str(nums.split('|').index(s.group(1))),
            line,
        )
        for line in data
    ]
    return part_a_solver(new_data)

if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
