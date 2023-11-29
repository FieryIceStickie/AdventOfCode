from typing import Iterator, Iterable
from collections import deque


deltas = (-1, 1j, 1, -1j)
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

def windowed(iterable: Iterable, n: int):
    it = iter(iterable)
    window = deque(islice(it, n-1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)
