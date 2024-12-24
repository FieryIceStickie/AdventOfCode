from collections import Counter
from itertools import pairwise, islice, batched
from collections.abc import Iterator
from typing import TextIO
import multiprocessing


def parser(raw_data: TextIO):
    return [*map(int, raw_data.read().splitlines())]


def full_solver(data: list[int]):
    p1 = 0
    p2 = Counter()
    with multiprocessing.Pool() as pool:
        for num, counts in pool.imap_unordered(
            solve, batched(data, 175), chunksize=1,
        ):
            p1 += num
            p2 += counts
    return p1, max(p2.values())


def gen_seq(num: int) -> Iterator[int]:
    yield num
    while True:
        num ^= num << 6 & 0xffffff
        num ^= num >> 5 & 0xffffff
        num ^= num << 11 & 0xffffff
        yield num


def solve(data: list[int]) -> tuple[int, Counter]:
    p1 = 0
    p2 = Counter()
    for seed in data:
        seen = set()
        nums = gen_seq(seed)
        window = [n % 10 for n in islice(nums, None, 4)]
        diffs = [9 + j - i for i, j in pairwise(window)]
        diff = sum(v * 19 ** i for i, v in enumerate(diffs[::-1]))
        prev = window[-1]
        for num in islice(nums, None, 1996):
            price = num % 10
            diff = 9 + price - prev + diff * 19 % 130321
            prev = price
            if diff in seen: continue
            seen.add(diff)
            if price: p2[diff] += price
        p1 += next(nums)
    return p1, p2


if __name__ == '__main__':
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = 'input.txt'
    else:
        path = test_path if testing else 'input.txt'

    with open(path, 'r') as file:
        data = parser(file)
    import time
    st = time.perf_counter()
    print(*full_solver(data))
    ed = time.perf_counter()
    print(ed - st)
