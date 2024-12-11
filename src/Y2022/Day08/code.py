from math import prod

import numpy as np


def parser(filename: str):
    with open(filename, 'r') as file:
        rows = file.read().splitlines()
        shape = len(rows), len(rows[0])
        return np.array([i for row in rows for i in row], dtype=int).reshape(shape), shape

def part_a_solver(arr: np.ndarray, shape: tuple[int, int]):
    row_len, col_len = shape
    visible = {*range(row_len),
                  *(i * 1j for i in range(col_len)),
                  *(complex(i, col_len - 1) for i in range(row_len)),
                  *(complex(row_len - 1, i) for i in range(col_len))}

    for (row_idx, col_idx), height in np.ndenumerate(arr):
        if row_idx in (0, row_len - 1) or col_idx in (0, col_len - 1):
            continue
        directions = arr[row_idx - 1::-1, col_idx], \
            arr[row_idx, col_idx + 1:], \
            arr[row_idx + 1:, col_idx], \
            arr[row_idx, col_idx - 1::-1]
        if any(np.all(height > i) for i in directions):
            visible.add(complex(row_idx, col_idx))
    return len(visible)


def part_b_solver(arr: np.ndarray, shape: tuple[int, int]):
    row_len, col_len = shape
    max_view = 0
    for (row_idx, col_idx), height in np.ndenumerate(arr):
        if row_idx in (0, row_len - 1) or col_idx in (0, col_len - 1):
            continue
        directions = arr[row_idx - 1::-1, col_idx], \
            arr[row_idx, col_idx + 1:], \
            arr[row_idx + 1:, col_idx], \
            arr[row_idx, col_idx - 1::-1]
        view_score = prod(score + 1 if
                          (score := np.argmax(bool_arr := (i >= height))) or np.any(bool_arr) else
                          len(i) for i in directions)
        max_view = max(max_view, view_score)
    return max_view


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(*inputs))
    print(part_b_solver(*inputs))
