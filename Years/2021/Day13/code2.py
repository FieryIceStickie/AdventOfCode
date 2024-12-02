import re
from typing import Any

import numpy as np

from Tools.Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = test_path
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        lines = file.read().splitlines()
        split_idx = lines.index('')
        dot_indices = np.array([i.split(',') for i in lines[:split_idx]], dtype=int)
        instructions = (re.match(r'fold along ([xy])=(\d+)', i).groups() for i in lines[split_idx + 1:])
        instructions = np.array([(0 if i == 'x' else 1, j) for i, j in instructions], dtype=int)
        return dot_indices, instructions


def solver(dot_indices: np.ndarray, instructions: np.ndarray) -> Any:
    for axis, fold in instructions:
        dot_indices_arg = np.argsort(dot_indices[:, axis])
        dot_indices = dot_indices[dot_indices_arg]
        fold_idx = np.searchsorted(dot_indices[:, axis], fold)
        upper_fold, lower_fold = dot_indices[:fold_idx], dot_indices[fold_idx:]
        if axis:
            lower_fold = np.apply_along_axis(lambda x: np.array((x[0], 2*fold-x[1])), 1, lower_fold)
        else:
            lower_fold = np.apply_along_axis(lambda x: np.array((2*fold-x[0], x[1])), 1, lower_fold)
        dot_indices = np.unique(np.concatenate((upper_fold, lower_fold)), axis=0)
    return dot_indices


def display(dot_indices) -> None:
    x = np.zeros((6, 40))
    for i, j in dot_indices:
        x[j, i] = 1
    for i in x:
        for j in i:
            print('#' if j else '.', end=' ')
        print('')


if __name__ == '__main__':
    answer = solver(*parser(
        file_name='input.txt',
        testing=False))
    display(answer)
