import operator
from functools import reduce
from typing import Any

import numpy as np

from Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            return np.array([list(i) for i in lines], dtype=int)
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            lines = file.read().splitlines()
            return np.array([list(i) for i in lines], dtype=int)
    return inputs


def gradient(x1: int, x2: int) -> -1 | 0 | 1:
    """
    Takes two numbers and returns the gradient of them
    :param x1: The first point
    :param x2: The second point
    :return: The gradient
    """
    if x2 > x1:
        return 1
    elif x1 > x2:
        return -1
    else:
        return 0


class GradientMap:
    def __init__(self, vent_map: np.ndarray):
        self.vent_map = vent_map
        self.hori_grads = []
        self.vert_grads = []
        self.hori_len, self.vert_len = np.shape(self.vent_map)

    def save_grad(self, arr: np.ndarray, orientation: 0 | 1):
        if orientation:
            self.hori_grads.append(arr)
        else:
            self.vert_grads.append(arr)

    def finish_save(self):
        self.hori_grads = np.array(self.hori_grads)
        self.vert_grads = np.array(self.vert_grads)

    def get_surrounding_points(self, xn: int, yn: int, *, keep_none: bool = True) -> list[tuple[int, int]]:
        # down, up, right, left
        pts = [(xn + 1, yn), (xn - 1, yn), (xn, yn + 1), (xn, yn - 1)]
        if keep_none:
            pts = [(x, y) if self.hori_len > x >= 0 and self.vert_len > y >= 0 else None for x, y in pts]
            pts = [i if (i is not None and self.vent_map[i] != 9) else None for i in pts]
        else:
            pts = [(x, y) for x, y in pts if self.hori_len > x >= 0 and self.vert_len > y >= 0]
            pts = [i for i in pts if self.vent_map[i] != 9]
        return pts

    def get_surrounding_hills(self, xn: int, yn: int) -> list[tuple[int, int]]:
        grads = [(yn, xn), (yn, xn - 1), (xn, yn), (xn, yn - 1)]
        vert_grads, hori_grads = grads[:2], grads[2:]
        vert_grads = [(y, x) if self.vert_len > y >= 0 and
                                self.hori_len - 1 > x >= 0 else None for y, x in vert_grads]
        hori_grads = [(x, y) if self.vert_len - 1 > y >= 0 and
                                self.hori_len > x >= 0 else None for x, y in hori_grads]
        grads = vert_grads + hori_grads
        surrounding_pts = self.get_surrounding_points(xn, yn, keep_none=True)
        hills = [v for i, v in enumerate(surrounding_pts) if (grads[i] is not None and v is not None and
                 (self.vert_grads, self.hori_grads)[i > 1][grads[i]] == (1, -1, 1, -1)[i])]
        return hills


def find_lows(tube: np.ndarray, obj: GradientMap, orientation: 0 | 1) -> np.ndarray:
    gradient_array = np.array([(i, gradient(v, tube[i + 1])) for i, v in enumerate(tube[:-1])])
    obj.save_grad(gradient_array[:, 1], orientation)
    low_candidates = tube[:1].tolist() if gradient_array[0, 1] == 1 else [-1]
    for i, g in gradient_array:
        if i == 0:
            continue
        low_candidates.append(tube[i] if (gradient_array[i - 1, 1] == -1 and g == 1) else -1)
    low_candidates.append(tube[-1] if gradient_array[-1, 1] == -1 else -1)
    return np.array(low_candidates)


def surround_gradients(xn: int, yn: int) -> list[tuple[int, int], ...]:
    """
    [down, up, right, left]
    """
    return [(yn, xn), (yn, xn - 1), (xn, yn), (xn, yn - 1)]


def find_max_three(iterable: list | tuple) -> tuple[int, int, int]:
    if len(iterable) < 3:
        raise NotImplementedError
    low = iterable[0]
    mid = iterable[1]
    high = iterable[2]
    low, mid, high = sorted((low, mid, high))
    for i in iterable[3:]:
        if i > low:
            low = i
            low, mid, high = sorted((low, mid, high))
    return low, mid, high


def solver(inputs: Any) -> Any:
    obj = GradientMap(inputs)
    horizontal_candidates = np.apply_along_axis(find_lows, 1, inputs, obj, 1)
    vertical_candidates = np.apply_along_axis(find_lows, 0, inputs, obj, 0)
    obj.finish_save()
    low_points = np.apply_along_axis(lambda xi: xi[0] if xi[0] == xi[1] else -1, 1,
                                     tuple(zip(horizontal_candidates, vertical_candidates)))
    low_point_indices = np.nonzero(low_points + 1)
    basin_sizes = []
    for xn, yn in np.column_stack(low_point_indices):
        unchecked_points = obj.get_surrounding_points(xn, yn, keep_none=False)
        checked_points = [(xn, yn)]
        while unchecked_points:
            new_points = []
            for x0, y0 in unchecked_points:
                new_points += obj.get_surrounding_hills(x0, y0)
            new_points = [i for i in new_points if i not in checked_points]
            checked_points += unchecked_points
            unchecked_points = []
            for i in new_points:
                if i not in unchecked_points:
                    unchecked_points.append(i)
        basin_sizes.append(len(checked_points))
    return reduce(operator.mul, find_max_three(basin_sizes))


def display(risk) -> None:
    print(risk)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='input.txt',
        testing=False))
    display(answer)
