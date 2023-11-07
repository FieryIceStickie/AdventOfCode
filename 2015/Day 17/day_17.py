from collections import Counter
from typing import TextIO


from path_stuff import *


def parser(raw_data: TextIO):
    return Counter(int(i) for i in raw_data.read().splitlines())


def part_a_solver(sizes: Counter[int]):
    variants = sorted(sizes, reverse=True)

    def solve(curr: int, c_idx: int = 0):
        if curr == 0:
            return 1
        elif curr < 0:
            return 0
        res = 0
        for idx, size in enumerate(variants[c_idx:], start=c_idx):
            if not sizes[size]:
                continue
            sizes[size] -= 1
            res += solve(curr - size, idx)
            if sizes[size]:
                res += solve(curr - size, idx+1)
            sizes[size] += 1
        return res
    return solve(150 if not testing else 25)


def part_b_solver(sizes: Counter[int]):
    variants = sorted(sizes, reverse=True)
    c_min = len(sizes)
    res = 0

    def solve(curr: int, c_idx: int = 0, count: int = 0, bag = ()):
        nonlocal c_min, res
        if count > c_min:
            return
        elif curr == 0:
            if c_min > count:
                res = 0
                c_min = count
            res += 1
            return
        elif curr < 0:
            return

        for idx, size in enumerate(variants[c_idx:], start=c_idx):
            if not sizes[size]:
                continue
            sizes[size] -= 1
            solve(curr - size, idx, count + 1)
            if sizes[size]:
                solve(curr - size, idx + 1, count + 1)
            sizes[size] += 1

    solve(150 if not testing else 25)
    return res


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day 17/day_17.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
