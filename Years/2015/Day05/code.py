import re
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data: list[str]):
    pattern = re.compile(r'(?=.*(?:[aeiou]).*(?:[aeiou]).*(?:[aeiou]))(?=.*(.)\1)(?!.*(?:ab|cd|pq|xy)).+')
    return sum(1 for string in data if pattern.match(string))


def part_b_solver(data: list[str]):
    pattern = re.compile(r'(?=.*(..).*\1)(?=.*(.).\2).+')
    return sum(1 for string in data if pattern.match(string))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
