from typing import TextIO

import numpy as np
import scipy

from Years.path_stuff import *


def parser(raw_data: TextIO):
    # noinspection PyTypeChecker
    data = np.genfromtxt(
        raw_data,
        delimiter=1,
        comments=None,
        dtype=np.str_,
    )
    return np.where(data == '.', np.full(data.shape, '11'), data)


def part_a_solver(data):
    data = np.asarray(
        np.where(np.char.isdigit(data), data, '-1211'),
        dtype=np.int16,
    )
    data = np.where(data == 11, np.full(data.shape, -1, dtype=np.int16), data)
    kernels = [
        [[0, 0, 1, 1, 1, 1, 1],
         [0, 0, 1, 0, 0, 0, 1],
         [0, 0, 1, 1, 1, 1, 1]],
        [[0, 0, 121, 11, 1]],

        [[1, 1, 1, 1, 1],
         [1, 0, 0, 0, 1],
         [1, 1, 1, 1, 1]],
        [[121, 11, 1]],

        [[1, 1, 1, 1, 1, 0, 0],
         [1, 0, 0, 0, 1, 0, 0],
         [1, 1, 1, 1, 1, 0, 0]],
        [[121, 11, 1, 0, 0]],


        [[0, 1, 1, 1, 1],
         [0, 1, 0, 0, 1],
         [0, 1, 1, 1, 1]],
        [[0, 11, 1]],

        [[1, 1, 1, 1, 0],
         [1, 0, 0, 1, 0],
         [1, 1, 1, 1, 0]],
        [[11, 1, 0]],


        [[1, 1, 1],
         [1, 0, 1],
         [1, 1, 1]],
        [[1]],
    ]
    (
        d__s_kernel, d__d_kernel,
        _d_s_kernel, _d_d_kernel,
        __ds_kernel, __dd_kernel,
        d_s_kernel, d_d_kernel,
        _ds_kernel, _dd_kernel,
        ds_kernel, dd_kernel
    ) = (scipy.signal.convolve2d(data + 1, np.flip(np.array(kernel, dtype=np.int16)), mode='same') for kernel in kernels)
    hundred_mask = (
        (d__s_kernel < 0)
        & (d__d_kernel % 11 > 0)
        & (d__d_kernel // 11 % 11 > 0)
        & (d__d_kernel > 121)
    )
    ten_mask = (
        (_d_s_kernel < 0)
        & (_d_d_kernel % 11 > 0)
        & (_d_d_kernel // 11 % 11 > 0)
        & (_d_d_kernel > 121)
        |
        (d_s_kernel < 0)
        & (d_d_kernel % 11 > 0)
        & (d_d_kernel > 11)
    ) & np.logical_not(hundred_mask)
    one_mask = (
        (__ds_kernel < 0)
        & (__dd_kernel % 11 > 0)
        & (__dd_kernel // 11 % 11 > 0)
        & (__dd_kernel > 121)
        |
        (_ds_kernel < 0)
        & (_dd_kernel % 11 > 0)
        & (_dd_kernel > 11)
        |
        (ds_kernel < 0)
        & (dd_kernel > 0)
    ) & np.logical_not(hundred_mask | ten_mask)
    return (100 * data[hundred_mask].sum()
            + 10 * data[ten_mask].sum()
            + data[one_mask].sum())


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        parsed_data = parser(file)

    print(part_a_solver(parsed_data))