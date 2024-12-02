import re
from typing import TextIO

import numpy as np

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [[int(num) for num in re.findall(r'-?\d+', line)] for line in raw_data.read().splitlines()]


def solve(data: list[list[int]]) -> tuple[int, int]:
    data = np.array(data, dtype=np.int64)
    constraint_matrix = data[:, :4].T
    calorie_vec = data[:, -1]
    c1_max = 0
    c2_max = 0
    value = np.zeros((4,), dtype=np.int64)
    for i in range(100):
        value[0] = i
        for j in range(100 - i):
            value[1] = j
            for k in range(100 - i - j):
                value[2] = k
                value[3] = 100 - i - j - k
                res = constraint_matrix @ value
                score = np.all(res > 0) and np.prod(res)
                c1_max = max(c1_max, score)
                if calorie_vec @ value == 500:
                    c2_max = max(c2_max, score)
    return c1_max, c2_max


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solve(data))

