import re
from functools import reduce
from typing import TextIO

from Tools.Python.path_stuff import *


def full_solver(raw_data: TextIO):
    return (
            (
                step_func := lambda x, y: 17 * (x + y) % 256,
                hash_func := lambda string: reduce(step_func, map(ord, string), 0)
            )
            and
            (
                (lambda box_state, p1:
                 (
                     p1,
                     sum(
                         sum(box_idx * focal_idx * int(focal_len) for focal_idx, focal_len in
                             enumerate(box.values(), start=1))
                         for box_idx, box in enumerate(box_state, start=1)
                     )
                 ))
                    (
                    *reduce(
                        lambda state, instruction: (
                            getattr(
                                state[0][hash_func(re.match(r'\w+', instruction).group(0))],
                                '__setitem__' if '=' in instruction else 'pop'
                            )(*re.split(r'=|(?=-)', instruction))
                            and state[0] or state[0],
                            state[1] + hash_func(instruction)
                        ),
                        raw_data.read().split(','),
                        ([{} for _ in range(256)], 0))
                )))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        print(*full_solver(file))
