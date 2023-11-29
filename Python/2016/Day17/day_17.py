from collections import deque
from hashlib import md5
from typing import TextIO

from Python.path_stuff import *
from Python.Tools.utils import inverse_facing_dict


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_solver(passcode: str):
    active = deque([(0, '')])
    inv_d = inverse_facing_dict['letters']
    while active:
        current, path = active.popleft()
        if current == 3+3j:
            return path
        for d, b in zip((-1, 1, -1j, 1j), md5((passcode + path).encode()).hexdigest()):
            if 'a' < b < 'g':
                loc = current + d
                new_path = path + inv_d[d]
                if 4 > loc.real >= 0 <= loc.imag < 4:
                    active.append((loc, new_path))
    else:
        return None


def part_b_solver(passcode: str):
    active = deque([(0, '')])
    inv_d = inverse_facing_dict['letters']
    c_max = 0
    while active:
        current, path = active.popleft()
        if current == 3+3j:
            c_max = max(len(path), c_max)
            continue
        for d, b in zip((-1, 1, -1j, 1j), md5((passcode + path).encode()).hexdigest()):
            if 'a' < b < 'g':
                loc = current + d
                new_path = path + inv_d[d]
                if 4 > loc.real >= 0 <= loc.imag < 4:
                    active.append((loc, new_path))
    return c_max


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day17/day_17.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
