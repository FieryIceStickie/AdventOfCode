from typing import Iterator, Iterable
from collections import deque
from itertools import islice


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
    icon_dict = {0+0j: 's', **{i: '#' for i in visited},**icons}
    print(*(''.join(icon_dict.get(complex(x, y), visited_icon)
                    for x in range(real_min, real_max + 1))
            for y in range(imag_min, imag_max + 1)),
          sep='\n', end='\n\n')

def switch(z: complex):
    return z.imag + 1j*z.real
