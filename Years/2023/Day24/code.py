import re
from itertools import batched, combinations
from math import gcd, lcm
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return [
        [*batched(map(int, line), 3)]
        for line in re.findall(
            r'(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*@\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)',
            raw_data.read()
        )
    ]


def part_a_solver(data):
    lb = 200000000000000 if not testing else 7
    ub = 400000000000000 if not testing else 27
    c = 0
    for ((*p1, _), (*v1, _)), ((*p2, _), (*v2, _)) in combinations(data, 2):
        (x1, y1), (a1, b1), (x2, y2) = p1, v1, p2
        t, s, g = get_intersect_values(p1, v1, p2, v2)
        if not g:
            c += (x2 - x1) / a1 == (y2 - y1) / b1
            continue
        t /= g
        s /= g
        if t < 0 or s < 0:
            continue
        c += all(lb <= v <= ub for v in (x1 + t*a1, y1+t*b1))
    return c


def get_intersect_values(p1: tuple[int, int], v1: tuple[int, int],
                         p2: tuple[int, int], v2: tuple[int, int]) -> tuple[int, int, int]:
    """
    Cramer's rule on
    p1 + t*v1 = p2 + s*v2
    t*v1 - s*v2 = p2 - p1
    :return: (t*g, s*g, g) so that t and s remain ints
    """
    (x1, y1), (x2, y2), (a1, b1), (a2, b2) = p1, p2, v1, v2
    px, py = x2 - x1, y2 - y1
    g = b1*a2 - a1*b2
    t = a2*py - b2*px
    s = py*a1 - px*b1
    return t, s, g


def det(m: list[list[int]], cols: tuple[int, ...] = ()) -> int:
    if len(m) == 1:
        return next(v for i, v in enumerate(m[0]) if i not in cols)
    rtn = 0
    parity = 1
    for c, v in enumerate(m[0]):
        if c not in cols:
            rtn += v * parity * det(m[1:], cols + (c,))
            parity = -parity
    return rtn


def replace(m: list[list[int]], col: int, b: list[int]) -> list[list[int]]:
    return [
        [b[r] if c == col else v for c, v in enumerate(row)]
        for r, row in enumerate(m)
    ]


def part_b_solver(data):
    m, b = zip(*[
        ([bi, -ai, zi*bi - yi*ci, xi*ci-zi*ai, ci], xi*bi-yi*ai)
        for ((xi, yi, zi), (ai, bi, ci)) in data[:5]
    ])
    d = det(m)
    x, y, a, b, _ = [[det(replace(m, i, b)), d] for i in range(5)]
    for num in (x, y, a, b):
        g = gcd(num[0], d)
        num[0] //= g
        num[1] //= g
    g = lcm(*[d for _, d in (x, y, a, b)])
    for num in (x, y, a, b):
        h = g // num[1]
        num[0] *= h
        num[1] *= h

    # Integer-ize x, y, a, b
    (x, _), (y, _), (a, _), (b, _) = x, y, a, b

    # x and y need to be shifted to be 0 mod g
    # a*t = x mod g
    # t = x a^-1 mod g
    # similarly
    # t = y b^-1 mod g
    x_shift = x * pow(a, -1, g) % g
    y_shift = y * pow(b, -1, g) % g
    assert x_shift == y_shift
    x -= a*x_shift
    y -= b*y_shift
    assert not x % g and not y % g
    x //= g
    y //= g
    z = -x_shift
    p = (x, y)
    v = (a, b)

    # We now have p and v in integer form
    # we need to find where we collide with two points, and then
    # we can find the actual vector by taking the vector between the collision and dividing by time
    # and then trace back to the start

    [(*p1, z1), (*v1, c1)], [(*p2, z2), (*v2, c2)] = data[:2]
    (x1, y1), (a1, b1) = p1, v1
    (x2, y2), (a2, b2) = p2, v2
    t1, s1, g1 = get_intersect_values(p1, v1, p, v)
    t2, s2, g2 = get_intersect_values(p2, v2, p, v)
    # t/g would be the time here
    assert not t1 % g1
    assert not t2 % g2
    t1 //= g1
    t2 //= g2
    assert not s1 % g1
    assert not s2 % g2
    s1 //= g1
    s2 //= g2
    assert z1 + t1*c1 == z + s1*g
    assert z2 + t2*c2 == z + s2*g

    u1, w1 = x1 + t1*a1, y1+t1*b1
    u2, w2 = x2 + t2*a2, y2+t2*b2
    assert not (u2 - u1) % (t2 - t1)
    assert not (w2 - w1) % (t2 - t1)
    dx, dy = ((u2 - u1) // (t2 - t1), (w2 - w1) // (t2 - t1))
    assert not dx % a
    dz = g * dx // a
    z = z1 + t1*c1
    p = (u1 - t1*dx, w1 - t1*dy, z - t1*dz)
    return sum(p)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
