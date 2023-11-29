from typing import TextIO
from collections.abc import Iterator

from Python.path_stuff import *
from itertools import pairwise


def parser(raw_data: TextIO):
    return raw_data.read()


alphabet = 'abcdefghijklmopqrstuvwxyz'
*triplets, = map(''.join, zip(alphabet, alphabet[1:], alphabet[2:]))
*doubles, = map(''.join, zip(alphabet, alphabet))
inc_dict = dict(pairwise('abcdefghjkmnpqrstuvwxyz'))


def increment(start: str) -> Iterator[str]:
    *rtn, = start[::-1]
    while True:
        for i, v in enumerate(rtn):
            if v == 'z':
                rtn[i] = 'a'
            else:
                rtn[i] = inc_dict[v]
                break
        yield ''.join(rtn[::-1])


def solve(start: str):
    return next(i for i in increment(start)
                if all(c not in i for c in 'ilo')
                and any(t in i for t in triplets)
                and sum(d in i for d in doubles) >= 2)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2015/Day 11/day_11.txt', 'r') as file:
        data = parser(file)

    print(res := solve(data))
    print(solve(res))
