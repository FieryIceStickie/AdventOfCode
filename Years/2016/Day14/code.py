import re
from collections import defaultdict, deque
from collections.abc import Callable
from hashlib import md5
from itertools import count, repeat
from typing import TextIO

from Years.path_stuff import *


def parser(raw_data: TextIO):
    return raw_data.read()


def solve(pad: str, hashing_func: Callable[[int], str]) -> list[int]:
    keys = []
    active = defaultdict(deque)
    countdown = deque([0] * 1000)
    idxs = {}
    threes = re.compile(r'(\w)\1{2}')
    pad += '{}'
    remaining = -1
    for c in count(0):
        if not remaining:
            break
        remaining -= 1
        h = hashing_func(pad.format(c))
        for k in [k for k, v in active.items() if v and k * 5 in h]:
            keys.extend(active[k])
            for i in active[k]:
                del idxs[i]
            del active[k]
        if remaining < 0 and len(keys) >= 64:
            remaining = 1000
        if match := threes.search(h):
            m = match.group(1)
            active[m].append(c)
            idxs[c] = m
            countdown.append(c)
        else:
            countdown.append(0)
        if (idx := countdown.popleft()) and idx in idxs:
            active[idxs[idx]].popleft()
            del idxs[idx]
    return sorted(keys)


def part_a_solver(data: str):
    def hashing_func(s: str) -> str:
        return md5(s.encode()).hexdigest()
    return solve(data, hashing_func)[63]


def part_b_solver(data: str):
    def hashing_func(s: str) -> str:
        for _ in repeat(0, times=2017):
            s = md5(s.encode()).hexdigest()
        return s
    return solve(data, hashing_func)[63]


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
