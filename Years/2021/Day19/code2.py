from collections import Counter
from itertools import permutations, product
from typing import Any

import numpy as np

from Years.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = test_path
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        scanners = []
        for line in file.read().split('\n\n'):
            scanners.append(np.array(tuple(tuple(int(ii) for ii in i.split(',')) for i in line.splitlines()[1:])))
        return tuple(scanners)


def solver(scans: tuple[np.ndarray, ...]) -> Any:
    scanner_loc_dict = {0: np.zeros(3)}
    beacons = set((x, y, z) for x, y, z in scans[0])
    orientations = (lambda vec: np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).dot(vec),
                    lambda vec: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]).dot(vec),
                    lambda vec: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]).dot(vec),

                    lambda vec: np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]]).dot(vec),
                    lambda vec: np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]).dot(vec),
                    lambda vec: np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]).dot(vec),

                    lambda vec: np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]).dot(vec),
                    lambda vec: np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]).dot(vec),
                    lambda vec: np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]).dot(vec),

                    lambda vec: np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]).dot(vec),
                    lambda vec: np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]]).dot(vec),
                    lambda vec: np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]).dot(vec),

                    lambda vec: np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]).dot(vec),
                    lambda vec: np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]]).dot(vec),
                    lambda vec: np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]]).dot(vec),

                    lambda vec: np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]).dot(vec),
                    lambda vec: np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]).dot(vec),
                    lambda vec: np.array([[0, 0, -1], [1, 0, 0], [0, -1, 0]]).dot(vec),

                    lambda vec: np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]).dot(vec),
                    lambda vec: np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]]).dot(vec),
                    lambda vec: np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]]).dot(vec),

                    lambda vec: np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]]).dot(vec),
                    lambda vec: np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]]).dot(vec),
                    lambda vec: np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]]).dot(vec),
                    )
    previous_scanner_len = 0
    while (current_len := len(scanner_loc_dict)) < len(scans):
        if current_len == previous_scanner_len:
            raise ValueError
        previous_scanner_len = current_len
        for scanner_num, scanner_beacons in enumerate(scans):
            if scanner_num in scanner_loc_dict:
                continue
            for perm in orientations:
                deltas = Counter()
                for vec1, vec2 in product(beacons, scanner_beacons):
                    delta = perm(vec2) - vec1
                    deltas[tuple(delta)] += 1
                top_delta, top_delta_count = deltas.most_common(1)[0]
                if top_delta_count >= 12:
                    scanner_loc_dict[scanner_num] = top_delta
                    for vector in scanner_beacons:
                        beacons.add(tuple(perm(vector) - top_delta))
                    break
    max_distance = 0
    for vec1, vec2 in permutations(scanner_loc_dict.values(), 2):
        if (distance := sum(abs(i - j) for i, j in zip(vec1, vec2))) > max_distance:
            max_distance = distance
    return max_distance


def display(distance) -> None:
    print(distance)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='input.txt',
        testing=False))
    display(answer)
