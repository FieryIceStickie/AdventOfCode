import re
from operator import eq, gt, lt
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    match_data, sue_data = raw_data.read().split('\n\n')
    match_dict = {k: int(v) for k, v in (line.split(': ') for line in match_data.split('\n'))}
    sue_dicts = [{k: int(v) for k, v in re.findall(r'(\w+): (\d+)(?:, |$)', line)}
                 for line in sue_data.split('\n')]
    return match_dict, sue_dicts


def part_a_solver(match_dict: dict[str, int], sue_dicts: list[dict[str, int]]):
    return next(i for i, sue in enumerate(sue_dicts, start=1)
                if all(match_dict[k] == v for k, v in sue.items()))


def part_b_solver(match_dict: dict[str, int], sue_dicts: list[dict[str, int]]):
    op_dict = {'cats': gt, 'trees': gt, 'pomeranians': lt, 'goldfish': lt}
    return next(i for i, sue in enumerate(sue_dicts, start=1)
                if all(op_dict.get(k, eq)(v, match_dict[k]) for k, v in sue.items()))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(*data))
    print(part_b_solver(*data))
