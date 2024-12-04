from typing import TextIO

import scipy.fftpack.convolve

from Tools.Python.path_stuff import *

import numpy as np
import scipy as sp
import re


def parser(raw_data: TextIO):
    return raw_data.read()


def part_a_regex(w: int) -> re.Pattern:
    return re.compile(
        fr'(?<=SAM)(?=X)'
        fr'|X(?=MAS)'
        fr'|(?<=S.{{{w}}}A.{{{w}}})(?=M.{{{w}}}X)'
        fr'|(?<=X.{{{w}}})M(?=.{{{w}}}A.{{{w}}}S)'
        fr'|(?<=S.{{{w + 1}}})(?=A.{{{w + 1}}}M.{{{w + 1}}}X)'
        fr'|(?<=X.{{{w + 1}}}M.{{{w + 1}}})A(?=.{{{w + 1}}}S)'
        fr'|(?=S.{{{w - 1}}}A.{{{w - 1}}}M.{{{w - 1}}}X)'
        fr'|(?<=X.{{{w - 1}}}M.{{{w - 1}}}A.{{{w - 1}}})S',
        flags=re.S,
    )


def part_a_solver(data: str):
    keymaps = {
        'X': 0,
        'M': 1,
        'A': 2,
        'S': 3,
    }
    grid = np.array([[keymaps[v] for v in line] for line in data.splitlines()])
    base = 4 ** np.arange(4)
    kernels = [
        base[np.newaxis, :],
        base[:, np.newaxis],
        np.diag(base),
        np.flip(np.diag(base), axis=1),
    ]
    return sum(
        np.count_nonzero(np.isin(
            sp.signal.convolve2d(grid, kernel, mode='valid'),
            np.array([27, 228]),
        ))
        for kernel in kernels
    )


def part_b_solver(data: str):
    keymaps = {
        'X': 3,
        'M': 1,
        'A': 2,
        'S': -1,
    }
    grid = np.array([[keymaps[v] for v in line] for line in data.splitlines()])
    kernel = np.array([
        [7j, 0, 5j],
        [0, 1, 0],
        [5j, 0, 7j],
    ])
    return np.count_nonzero(sp.signal.convolve2d(grid, kernel, mode='valid') == 2)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
