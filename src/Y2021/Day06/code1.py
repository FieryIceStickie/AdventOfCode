from typing import Any

import numpy as np

from Tools.Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return file.read().split(',')
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            return file.read().split(',')
    return inputs


def fish_sim(fish: np.ndarray):
    while True:
        fish_birth_count = np.count_nonzero(fish == 0)
        fish = np.where(fish == 0, 7, fish)
        fish = np.concatenate((fish, np.full(fish_birth_count, 9, dtype=int))) - 1
        yield len(fish)


def solver(inputs: Any) -> Any:
    sim = fish_sim(np.array(inputs, dtype=int))
    population = 0
    for _ in range(80):
        population = next(sim)
    return population


def display(population) -> None:
    print(population)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
