from typing import TextIO
from itertools import batched
import re

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return batched(map(int, re.findall(r'\d+', raw_data.read())), 6)


def full_solver(data):
    p = [0, 0]
    for a, c, b, d, v1, v2 in data:
        det = a*d - b*c
        if not det:
            raise ValueError('Singular matrix')
        sgn = -1 if det < 0 else 1
        det = abs(det)
        for i, u1, u2 in [(0, v1, v2), (1, 10000000000000 + v1, 10000000000000 + v2)]:
            x1 = d * u1 - b * u2
            x2 = -c * u1 + a * u2
            x1 *= sgn
            x2 *= sgn
            if min(x1, x2) < 0:
                continue
            (q1, r1), (q2, r2) = map(divmod, (x1, x2), (det, det))
            if r1 or r2:
                continue
            p[i] += 3 * q1 + q2
    return *p,


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)
    print(*full_solver(data))
