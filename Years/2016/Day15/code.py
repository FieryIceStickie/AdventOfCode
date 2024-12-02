import re
from functools import reduce
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    pattern = re.compile(r'Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+)\.')
    return [(-int(n) - i, int(p))
            for i, (p, n) in enumerate(
            (pattern.match(row).groups() for row in raw_data.read().splitlines()), start=1
            )]


def mul_inv(n: int, b: int) -> tuple[int, int]:
    n %= b
    r0, s0 = b, 0
    r1, s1 = n, 1
    while True:
        q, r = divmod(r0, r1)
        if not r:
            break
        s = s0 - q * s1
        r0, s0 = r1, s1
        r1, s1 = r, s
    return s1, r1


def pairwise_crt(eqn1: tuple[int, int] | None, eqn2: tuple[int, int]) -> tuple[int, int] | None:
    if eqn1 is None:
        return None
    (n0, p0), (n1, p1) = eqn1, eqn2
    q, g = mul_inv(p0, p1)
    m, r = divmod(n1 - n0, g)
    if r:
        return None
    p = p0 * p1 // g
    return (p0 * q * m + n0) % p, p


def crt(*eqns: tuple[int, int]) -> tuple[int, int] | None:
    return reduce(pairwise_crt, eqns)


def part_a_solver(eqns: list[tuple[int, int]]):
    n, p = crt(*eqns)
    return n % p


def part_b_solver(eqns: list[tuple[int, int]]):
    n, p = crt(*eqns, (~len(eqns), 11))
    return n % p


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
