from functools import cache
from typing import TextIO

from Python.path_stuff import *

type ParsedData = list[tuple[str, tuple[int]]]


def parser(raw_data: TextIO) -> ParsedData:
    return [
        (
            record,
            (*map(int, groups.split(',')),)
        )
        for record, groups in map(str.split, raw_data.read().splitlines())
    ]


@cache
def solve(record: str, groups: tuple[int], tracking: bool = False) -> int:
    if not record:
        return not any(groups)
    elif not groups:
        return all(c in '.?' for c in record)

    elem = record[0]
    if elem == '.':
        if tracking:
            if groups[0]:
                return 0
            new_groups = tuple(groups[1:])
        else:
            new_groups = groups
        return solve(record[1:], new_groups, False)
    elif elem == '#':
        if not groups[0]:
            return 0
        *new_groups, = groups
        new_groups[0] -= 1
        new_groups = tuple(new_groups)
        return solve(record[1:], new_groups, True)
    elif elem == '?':
        if tracking:
            return solve(('#' if groups[0] else '.') + record[1:], groups, True)
        return sum(solve(c + record[1:], groups, False) for c in '.#')


def solver(data: ParsedData) -> tuple[int, ...]:
    return tuple(
        sum(solve.cache_clear() or solve(*args) for args in pdata)
        for pdata in (data, [('?'.join([record] * 5), groups * 5) for record, groups in data])
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        parsed_data = parser(file)

    print(*solver(parsed_data))
