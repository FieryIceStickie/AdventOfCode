from typing import TextIO
from itertools import cycle, accumulate
import re
from math import lcm

from Python.path_stuff import *


def parser(raw_data: TextIO) -> tuple[str, dict[str, tuple[str, str]]]:
    steps, paths = raw_data.read().split('\n\n')
    return steps, {node: (conn1, conn2) for node, conn1, conn2 in re.findall(r'(\w{3}) = \((\w{3}), (\w{3})\)', paths)}


def solver(steps: str, paths: dict[str, tuple[str, str]]) -> tuple[int, int]:
    return next(idx for idx, v in enumerate(accumulate(cycle(steps), lambda node, step: paths[node][step == 'R'], initial='AAA')) if v == 'ZZZ'), lcm(*[next(idx for idx, v in enumerate(accumulate(cycle(steps), lambda node, step: paths[node][step == 'R'], initial=node)) if v.endswith('Z')) for node in paths if node.endswith('A')])


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(*data))
