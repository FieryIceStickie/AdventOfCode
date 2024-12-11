import cProfile
import pstats
import re
from itertools import product
from typing import Any

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
        instructions = []
        for line in file.read().splitlines():
            state, x_min, x_max, y_min, y_max, z_min, z_max = [int(i) if i not in ('on', 'off') else i == 'on'
                                                               for i in re.match(
                    r'(on|off) x=([-\d]+)..([-\d]+),y=([-\d]+)..([-\d]+),z=([-\d]+)..([-\d]+)', line).groups()]
            if abs(x_min) > 50:
                break
            instructions.append((state, x_min, x_max, y_min, y_max, z_min, z_max))
        return instructions


def solver(inputs: Any) -> Any:
    points = {}
    for state, x_min, x_max, y_min, y_max, z_min, z_max in inputs:
        for x, y, z in product(range(x_min, x_max + 1), range(y_min, y_max + 1), range(z_min, z_max + 1)):
            points[(x, y, z)] = state
    return len([1 for i in points.values() if i])


def display(count) -> None:
    print(count)


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        answer = solver(parser(
            file_name='input.txt',
            testing=False))
        display(answer)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')
