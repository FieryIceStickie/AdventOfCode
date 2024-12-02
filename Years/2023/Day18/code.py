import re
from itertools import accumulate, pairwise
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return [(1j**'DRUL'.find(direction), int(steps), color)
            for direction, steps, color in re.findall(r'(\w) (\d+) \(#(\w{6})\)', raw_data.read())]


def part_a_solver(data):
    area = int(abs(sum((z1.conjugate() * z2).imag
               for z1, z2 in pairwise(accumulate(data, lambda z, state: z + state[0]*state[1], initial=0)))) / 2)
    boundary = sum(steps for _, steps, _ in data)
    interior = area - boundary//2 + 1
    return boundary + interior


def part_b_solver(data):
    modified_data = [int(color[:5], 16) * 1j**int(color[-1]) for _, _, color in data]
    area = int(abs(sum((z1.conjugate() * z2).imag
                       for z1, z2 in
                       pairwise(accumulate(modified_data, lambda z, d: z + d, initial=0)))) / 2)
    boundary = int(sum(map(abs, modified_data)))
    interior = area - boundary // 2 + 1
    return boundary + interior


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
