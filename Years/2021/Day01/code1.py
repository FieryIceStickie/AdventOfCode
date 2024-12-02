from typing import Any

import numpy as np

from Tools.Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return file.read().splitlines()
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            return file.read().splitlines()
    return inputs


def solver(inputs: Any) -> Any:
    depths = np.array(inputs, dtype=int)
    prev_depth = depths[0]
    i = 0
    for depth in depths[1:]:
        if depth > prev_depth:
            i += 1
        prev_depth = depth
    return i


def display(count) -> None:
    print(count)


if __name__ == '__main__':
    answer = solver(parser(
        0, 1, 2, 7, 4, 5,
        file_name='input.txt',
        testing=False))
    display(answer)
