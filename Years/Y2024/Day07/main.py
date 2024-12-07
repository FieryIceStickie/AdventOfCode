from collections.abc import Callable
from typing import TextIO
import operator

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [
        (int(target), [*map(int, nums.split())])
        for target, nums in (
            line.split(': ')
            for line in raw_data.read().splitlines()
        )
    ]


def check_solvable(target: int, nums: list[int], ops: list[Callable[[int, int], int]]):
    def solve(idx: int, num: int) -> bool:
        if idx == len(nums):
            return num == target
        elif num > target:
            return False
        for op in ops:
            if solve(idx + 1, op(num, nums[idx])):
                return True
        return False
    return solve(1, nums[0])


def part_a_solver(data: list[tuple[int, list[int]]]):
    return sum(
        target for target, nums in data
        if check_solvable(target, nums, [
            operator.add,
            operator.mul,
        ])
    )


def part_b_solver(data: list[tuple[int, list[int]]]):
    return sum(
        target for target, nums in data
        if check_solvable(target, nums, [
            operator.add,
            operator.mul,
            lambda x, y: int(f'{x}{y}'),
        ])
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
