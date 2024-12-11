from gc import enable
from typing import TextIO
import re

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_solver(data):
    return sum(int(i)*int(j) for i, j in re.findall(r'mul\((\d+),(\d+)\)', data))


def part_b_solver(data):
    s = 0
    e = True
    for m in re.finditer(r"mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", data):
        i, j, k, l = m.groups()
        if k:
            e = True
        elif l:
            e = False
        elif e:
            s += int(i) * int(j)
    return s


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
