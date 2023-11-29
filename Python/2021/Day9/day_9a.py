from typing import Any
import numpy as np


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            return np.array([list(i) for i in lines], dtype=int)
    if len(inputs) == 0 and testing:
        with open('test.txt', 'r') as file:
            lines = file.read().splitlines()
            return np.array([list(i) for i in lines], dtype=int)
    return inputs


def gradient(x1: int, x2: int) -> -1 | 0 | 1:
    if x2 > x1:
        return 1
    elif x1 > x2:
        return -1
    else:
        return 0


def find_lows(tube: np.ndarray) -> np.ndarray:
    gradient_array = np.array([(i, gradient(v, tube[i + 1])) for i, v in tuple(enumerate(tube))[:-1]])
    low_candidates = tube[:1].tolist() if gradient_array[0, 1] == 1 else [-1]
    for i, g in gradient_array:
        if i == 0:
            continue
        low_candidates.append(tube[i] if (gradient_array[i-1, 1] == -1 and g == 1) else -1)
    low_candidates.append(tube[-1] if gradient_array[-1, 1] == -1 else -1)
    return np.array(low_candidates)


def solver(inputs: Any) -> Any:
    horizontal_candidates = np.apply_along_axis(find_lows, 1, inputs)
    vertical_candidates = np.apply_along_axis(find_lows, 0, inputs)
    low_points = np.apply_along_axis(lambda x: x[0] if x[0] == x[1] else -1, 1,
                                     tuple(zip(horizontal_candidates, vertical_candidates)))
    return np.sum(low_points + 1)


def display(risk) -> None:
    print(risk)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='day_9.txt',
        testing=False))
    display(answer)
