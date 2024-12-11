from typing import Any

import numpy as np

from Tools.Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            points = []
            for line in lines:
                p1, p2 = line.split(' -> ')
                x1, y1 = p1.split(',')
                x2, y2 = p2.split(',')
                points.append(((x1, y1), (x2, y2)))
            return np.array(points, dtype=int)
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            lines = file.read().splitlines()
            points = []
            for line in lines:
                p1, p2 = line.split(' -> ')
                x1, y1 = p1.split(',')
                x2, y2 = p2.split(',')
                points.append(((x1, y1), (x2, y2)))
            return np.array(points, dtype=int)
    return inputs


def solver(inputs: Any) -> Any:
    vent_map = np.zeros((1000, 1000))
    for line in inputs:
        match line.tolist():
            case (x1, y1), (x2, y2) if x1 == x2:
                # Vertical Line
                y1, y2 = sorted((y1, y2))
                idx = np.linspace(y1, y2, num=y2-y1+1, dtype=int)
                vent_map[x1, idx] += 1
            case (x1, y1), (x2, y2) if y1 == y2:
                # Horizontal Line
                x1, x2 = sorted((x1, x2))
                idy = np.linspace(x1, x2, num=x2-x1+1, dtype=int)
                vent_map[idy, y1] += 1
            case (x1, y1), (x2, y2) if abs(y2-y1) == abs(x2-x1):
                # Diagonal Line
                # (1,1) -> (3,3)
                gradient = (y2-y1)//(x2-x1)
                x1, x2 = sorted((x1, x2))
                y1, y2 = sorted((y1, y2))
                idx = np.linspace(y1, y2, num=y2-y1+1, dtype=int)
                if gradient == -1:
                    idx = np.flip(idx, 0)
                idy = np.linspace(x1, x2, num=x2-x1+1, dtype=int)
                vent_map[idy, idx] += 1
            case _:
                raise NotImplementedError
    return np.count_nonzero(vent_map[vent_map > 1])


def display(count) -> None:
    print(count)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
