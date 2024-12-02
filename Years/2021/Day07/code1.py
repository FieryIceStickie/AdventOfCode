from typing import Any

import numpy as np

from Tools.Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return np.array(file.read().split(','), dtype=int)
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            return np.array(file.read().split(','), dtype=int)
    return inputs


def solver(inputs: Any) -> Any:
    return int(np.sum(np.abs(inputs - np.median(inputs))))


def display(fuel) -> None:
    print(fuel)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
