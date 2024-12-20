from collections.abc import Sequence, Iterator, Callable
from itertools import groupby
from typing import Iterator, Iterable, NamedTuple, Literal, overload, Protocol
from numbers import Real
import math
import operator

from attrs import frozen, define, field, evolve

deltas = (-1, 1j, 1, -1j)
corner_deltas = (-1 + 1j, 1 + 1j, 1 - 1j, -1 - 1j)
all_deltas = (-1, -1 + 1j, 1j, 1 + 1j, 1, 1 - 1j, -1j, -1 - 1j)
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
                    transpose: bool = False):
    if icons is None:
        icons = dict()
    if transpose:
        visited = {switch(z) for z in visited}
        icons = {switch(z): v for z, v in icons.items()}
    reals, imags = {int(i.real) for s in (visited, icons.keys()) for i in s}, \
        {int(i.imag) for s in (visited, icons.keys()) for i in s}
    real_min, real_max, imag_min, imag_max = min(reals), max(reals), min(imags), max(imags)
    icon_dict = {0 + 0j: 's', **{i: '#' for i in visited}, **icons}
    print(*(''.join(icon_dict.get(complex(x, y), visited_icon)
                    for x in range(real_min, real_max + 1))
            for y in range(imag_min, imag_max + 1)),
          sep='\n', end='\n\n')


def switch(z: complex):
    return z.imag + 1j * z.real


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


class Res(NamedTuple):
    p1: int
    p2: int

    def __add__(self, other):
        return Res(self.p1 + other.p1, self.p2 + other.p2)


def res_sum(iterable: Iterable[Res]) -> Res:
    return sum(iterable, Res(0, 0))


@operator.call
class _slice:
    def __getitem__(self, item):
        return item


# TODO: make this not slow and bloated
@frozen
class close_enumerate[M, R: Real]:
    """
    Takes a sequence of pairwise "close" points, and enumerates all sufficiently close points
    Similar to (
        (i, v, metric(v, target)) for i, v in enumerate(seq[slice_start:], start)
        if metric(v, target) <= threshold
    )
    Uses the "close" property to reduce elements searched
    R should support math.ceil

    Attributes
    ----------
    seq: Sequence[M]
        Satisfies all(metric(x, y) <= 1 for x, y in pairwise(seq))
    metric: Callable[[M, M], V]
    target: M
        Point to be close to
    threshold: V
        Radius that points have to lie within
    start: int
        Essentially turns seq into seq[slice_start:]
        Note: This differs from regular enumerate's start argument
    """
    seq: Sequence[M]
    metric: Callable[[M, M], R]
    target: M
    threshold: R
    _slice: slice = field(default=_slice[:])

    def __getitem__(self, item):
        match item:
            case slice():
                return evolve(self, slice=item)
            case _: return NotImplemented

    def __iter__(self):
        # TODO: fix negative indices by encapsulating in Interval class
        idx = 0 if self._slice.start is None else self._slice.start
        end = len(self.seq) if self._slice.stop is None else min(len(self.seq), self._slice.stop)
        while idx < end:
            v = self.seq[idx]
            dist = self.metric(v, self.target)
            if dist > self.threshold:
                idx += math.ceil(dist - self.threshold)
            else:
                yield idx, v, dist
                idx += 1


if __name__ == '__main__':
    pass