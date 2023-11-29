from typing import Any
import numpy as np
from math import floor, ceil


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return np.array(file.read().split(','), dtype=int)
    if len(inputs) == 0 and testing:
        with open('test.txt', 'r') as file:
            return np.array(file.read().split(','), dtype=int)
    return inputs


def solver(inputs: Any) -> Any:
    # noinspection PyTypeChecker
    mean = np.mean(inputs)
    lower = floor(mean)
    upper = ceil(mean)
    lower_distances = np.abs(inputs - lower)
    upper_distances = np.abs(inputs - upper)
    lower_fuel = int(np.sum(lower_distances * (lower_distances + 1) / 2))
    upper_fuel = int(np.sum(upper_distances * (upper_distances + 1) / 2))
    return min(lower_fuel, upper_fuel)


def display(fuel) -> None:
    print(fuel)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='day_7.txt',
        testing=False))
    display(answer)
