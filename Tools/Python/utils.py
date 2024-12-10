from collections import defaultdict
from collections.abc import Sequence
from typing import Self
from itertools import groupby
from typing import Iterator, Literal, Iterable

deltas = (-1, 1j, 1, -1j)
corner_deltas = (-1+1j, 1+1j, 1-1j, -1-1j)
all_deltas = (-1, -1+1j, 1j, 1+1j, 1, 1-1j, -1j, -1-1j)
facing_dict = {
    'letters': dict(zip('URDL', deltas)),
    'arrows': dict(zip('^>v<', deltas)),
}
inverse_facing_dict = {
    'letters': dict(zip(deltas, 'URDL')),
    'arrows': dict(zip(deltas, '^>v<')),
}


def complex_range(start: complex, end: complex) -> Iterator[complex]:
    if start.real == end.real:
        yield from (complex(start.real, i)
                    for i in range(int(start.imag), int(end.imag),
                                   -1 if start.imag > end.imag else 1))
    elif start.imag == end.imag:
        yield from (complex(i, start.imag)
                    for i in range(int(start.real), int(end.real),
                                   -1 if start.real > end.real else 1))
    else:
        raise NotImplemented

def try_int(inp: str) -> str | int:
    try:
        return int(inp)
    except ValueError:
        return inp

def display_visited(visited: set[complex], icons: dict[complex, str] = None,
                    visited_icon: str = '.',
                    transpose: bool = True):
    if icons is None:
        icons = dict()
    if transpose:
        visited = {switch(z) for z in visited}
        icons = {switch(z): v for z, v in icons.items()}
    reals, imags = {int(i.real) for s in (visited, icons.keys()) for i in s}, \
        {int(i.imag) for s in (visited, icons.keys()) for i in s}
    real_min, real_max, imag_min, imag_max = min(reals), max(reals), min(imags), max(imags)
    icon_dict = {0+0j: 's', **{i: '#' for i in visited}, **icons}
    print(*(''.join(icon_dict.get(complex(x, y), visited_icon)
                    for x in range(real_min, real_max + 1))
            for y in range(imag_min, imag_max + 1)),
          sep='\n', end='\n\n')


def switch(z: complex):
    return z.imag + 1j*z.real


def all_same[T](items: Iterable[T]) -> bool:
    g = groupby(items)
    next(g, None)
    return not next(g, False)


def odd_one_out[T](items: Iterable[T]) -> tuple[bool, int | None]:
    """
    Finds the index of the imposter
    :param items: an iterable
    :return: all_same(items), idx of imposter
    """
    items = [*items]
    try:
        idx = next(
            idx
            for idx, item in enumerate(items)
            if item != items[0]
        )
    except (StopIteration, IndexError):
        return True, None
    if idx == 1 and items[0] != items[2]:
        idx = 0
        item = items[1]
    else:
        item = items[0]
    if all_same([item] + items[idx + 1:]):
        return False, idx
    return False, None


def sgn(n: int) -> int:
    return (n > 0) - (n < 0)


def reversed_enumerate[T](seq: Sequence[T], /, start=None) -> Iterator[T]:
    if start is None:
        start = len(seq) - 1
    return (
        (start - i, v)
        for i, v in enumerate(reversed(seq))
    )


def sum_range(start: int | range, stop: int = None, step: int = 1) -> int:
    if isinstance(start, int):
        r = range(start, stop, step)
    else:
        r = start
    return len(r) * (2 * r.start + r.step * (len(r) - 1)) // 2


if __name__ == '__main__':
    pass
