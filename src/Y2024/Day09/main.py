from typing import TextIO
from itertools import chain, takewhile, repeat

from Tools.Python.path_stuff import *
from Tools.Python.utils.utils import sum_range


def parser(raw_data: TextIO):
    return [
        (int(size), idx // 2 if not idx % 2 else None)
        for idx, size in enumerate(raw_data.read())
    ]


def part_a_solver(data: list[tuple[int, int | None]]):
    *data, = chain.from_iterable(
        repeat(eyed, size)
        for idx, (size, eyed) in enumerate(data)
    )
    start = 0
    end = len(data) - 1
    while True:
        while data[start] is not None:
            start += 1
        while data[end] is None:
            end -= 1
        if start >= end:
            break
        data[start], data[end] = data[end], data[start]
    return sum(
        i * v
        for i, v in enumerate(
            takewhile(lambda x: x is not None, data)
        )
    )


def part_b_solver(data: list[tuple[int, int | None]]):
    idx = 0
    data = [
        [[idx, size, eyed], idx := idx + size][0]
        for size, eyed in data
    ]
    s = 0
    slots = data[1::2]
    for idx, size, eyed in data[::2][::-1]:
        for i, (slot_idx, slot_size, _) in enumerate(slots):
            if size <= slot_size or slot_idx > idx:
                break
        if slot_idx > idx:
            s += eyed * sum_range(idx, idx + size)
        else:
            s += eyed * sum_range(slot_idx, slot_idx + size)
            slots[i][0] += size
            slots[i][1] -= size
            if not slots[i][1]:
                slots.pop(i)
    return s


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
