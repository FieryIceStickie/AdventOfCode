import ast
from cmath import e, exp
from cmath import log as ln
from cmath import pi
from collections import Counter, defaultdict, deque
from itertools import *
from math import (
    cbrt, ceil, comb, dist, factorial, floor, gcd, isqrt, lcm, perm, sqrt
)
from typing import NamedTuple, TextIO

import numpy as np
from attrs import define, frozen

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data):
    return


def part_b_solver(data):
    return


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
