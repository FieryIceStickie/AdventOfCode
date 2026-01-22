from itertools import chain, islice
import warnings

import numpy as np

text = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

points = [complex(*map(int, line.split(","))) for line in text.splitlines()]

n = 10000
t = np.linspace(0, 1, n, endpoint=False)
dt = 1 / n


def integrate(p: complex, a: complex, b: complex) -> complex:
    # integral from p to q of dz/(z-p)
    return np.sum((b - a) / ((1 - t) * a + t * b - p) * dt)


def foo(points: list[complex], point: complex) -> complex:
    with warnings.catch_warnings(action='ignore'):
        res = sum(
            integrate(point, a, b)
            for a, b in zip(points, chain(islice(points, 1, None), [points[0]]))
        ) / (2j * np.pi)
    return complex(np.round(res, 1))


def display(z: complex) -> str:
    if z.real == 1:
        return "#"
    elif z.real == 0:
        return "."
    else:
        return "o"


grid = "\n".join(
    "".join(display(foo(points, x + 1j * y)) for x in range(15)) for y in range(10)
)
print(grid)
