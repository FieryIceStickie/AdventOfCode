import re
from bisect import bisect_right
from collections.abc import Iterable, Iterator
from functools import reduce
from itertools import batched
from operator import itemgetter
from typing import TextIO

from Tools.Python.path_stuff import *


# noinspection PyTypeChecker
def parser(raw_data: TextIO) -> tuple[list[int], list[tuple[int, ...]]]:
    seed_data, *map_data = raw_data.read().split('\n\n')
    *seeds, = map(int, re.findall(r'\d+', seed_data))
    maps = [
        sorted(
            [tuple(map(int, interval.split()))
             for interval in mapping.split('\n')[1:]],
            key=itemgetter(1),
        )
        for mapping in map_data
    ]
    return seeds, maps


def uniconvert(seeds: Iterable[int], mapping: list[tuple[int, ...]]) -> Iterator[int]:
    for seed in seeds:
        idx = bisect_right(mapping, seed, key=itemgetter(1))
        if not idx:
            yield seed
            continue
        dst, src, mrange = mapping[idx - 1]
        delta = seed - src
        if delta < mrange:
            yield dst + delta
        else:
            yield seed


def part_a_solver(seeds: list[int], maps: list[list[tuple[int, ...]]]):
    return min(reduce(uniconvert, maps, seeds))


def duoconvert(seeds: Iterable[tuple[int, int]], mapping: list[tuple[int, ...]]) -> Iterator[tuple[int, int]]:
    for start, rlen in seeds:
        start_idx = bisect_right(mapping, start, key=itemgetter(1))
        end_idx = bisect_right(mapping, start + rlen, key=itemgetter(1))
        # Range starts before any of the mappings
        if not start_idx:
            plen = min(rlen, mapping[0][1] - start)
            yield start, plen
            start += plen
            rlen -= plen
            if not rlen:
                continue
        for map_idx, (dst, src, mrange) in enumerate(mapping[start_idx - 1:end_idx], start=start_idx - 1):
            # Select portion of range overlapping with current mapping range
            delta = start - src
            if delta < mrange:
                plen = min(rlen, mrange - delta)
                yield dst + delta, plen
                start += plen
                rlen -= plen
            if not rlen:
                break

            # Select rest of range up to next mapping range
            if map_idx == end_idx - 1:
                plen = rlen
            else:
                plen = min(rlen, mapping[map_idx + 1][1] - start)
            if plen:
                yield start, plen
                start += plen
                rlen -= plen
            if not rlen:
                break


def part_b_solver(seeds: list[int], maps: list[list[tuple[int, ...]]]) -> int:
    return min(reduce(duoconvert, maps, batched(seeds, 2)))[0]


if __name__ == '__main__':
    testing = False
    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(*data))
    print(part_b_solver(*data))
