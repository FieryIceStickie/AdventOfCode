from collections.abc import Sequence, Iterable
from itertools import pairwise
from typing import TextIO
from functools import cache

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def make_grid(keypad):
    res = {
        x + 1j*y: v
        for x, row in enumerate(keypad.splitlines())
        for y, v in enumerate(row)
        if v != ' '
    }
    return res


NUM_KEYPAD = make_grid("""
789
456
123
 0A
""".strip('\n'))
INV_NUM_KEYPAD = {v: k for k, v in NUM_KEYPAD.items()}

DIR_KEYPAD = make_grid("""
 ^A
<v>
""".strip('\n'))
INV_DIR_KEYPAD = {v: k for k, v in DIR_KEYPAD.items()}
a_key = INV_DIR_KEYPAD['A']


def sgn(x: float) -> int:
    return (x > 0) - (x < 0)


def get_dirs(d: complex) -> list[complex]:
    d1, d2 = sgn(d.real), sgn(d.imag)
    if d1: yield d1
    if d2: yield d2 * 1j


d_dict = {
    d: INV_DIR_KEYPAD[s]
    for d, s in zip((-1, 1j, 1, -1j), '^>v<')
}


@cache
def all_paths(start: complex, end: complex, is_num: bool = False) -> Iterable[tuple[complex, ...]]:
    grid = NUM_KEYPAD if is_num else DIR_KEYPAD

    def solve(loc: complex):
        if loc == end:
            yield ()
            return
        for d in get_dirs(end - loc):
            if loc + d in grid:
                for p in solve(loc + d):
                    yield d_dict[d], *p
    return [*solve(start)]


def minimize_seq(keys: tuple[complex, ...], n: int, is_first: bool = False) -> int:
    if not n:
        return len(keys) - 1
    return sum(
        minimize_key(start, end, n - 1, is_first)
        for start, end in pairwise(keys)
    )


@cache
def minimize_key(start: complex, end: complex, n: int, is_first: bool) -> int:
    return min(
        minimize_seq((a_key, *path, a_key), n)
        for path in all_paths(start, end, is_first)
    )


def solve(data: list[str], num_keypads: int) -> int:
    return sum(
        minimize_seq(
            tuple(INV_NUM_KEYPAD[c] for c in f'A{code}'),
            num_keypads,
            True,
        ) * int(code[:-1])
        for code in data
    )


def full_solver(data: list[str]):
    return solve(data, 3), solve(data, 26)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    print(*full_solver(data))
