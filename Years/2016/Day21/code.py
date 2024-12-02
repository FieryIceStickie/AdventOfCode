import re
from typing import TextIO

from Years.path_stuff import *
from Years.Tools.utils import try_int


def parser(raw_data: TextIO):
    *patterns, = map(re.compile, [
        r'(swap) position (\d+) with position (\d+)',
        r'(swap) letter (\w) with letter (\w)',
        r'(rotate) (left|right) (\d+) steps?',
        r'(rotate) based on position of letter (\w)',
        r'(reverse) positions (\d+) through (\d+)',
        r'(move) position (\d+) to position (\d+)',
    ])
    return [next([*map(try_int, match.groups())] for pattern in patterns if (match := pattern.match(line)))
            for line in raw_data.read().splitlines()]


def part_a_solver(data: list[list[str | int]]):
    *string, = 'abcdefgh'
    size = len(string)
    for row in data:
        match row:
            case ['swap', int(x), int(y)]:
                string[x], string[y] = string[y], string[x]
            case ['swap', str(x), str(y)]:
                i, j = string.index(x), string.index(y)
                string[i], string[j] = y, x
            case ['rotate', 'left' | 'right' as direction, int(x)]:
                shift = (x * (-1) ** (direction == 'left')) % size
                string[:] = string[-shift:] + string[:-shift]
            case ['rotate', str(x)]:
                i = string.index(x)
                shift = (i + 1 + (i >= 4)) % size
                string[:] = string[-shift:] + string[:-shift]
            case ['reverse', int(x), int(y)]:
                string[x:y+1] = string[y:x-1 if x else None:-1]
            case ['move', int(x), int(y)]:
                string.insert(y, string.pop(x))
            case idk:
                raise ValueError(idk)
    return ''.join(string)


def part_b_solver(data: list[list[str | int]]):
    *string, = 'fbgdceah'
    size = len(string)
    for row in data[::-1]:
        match row:
            case ['swap', int(x), int(y)]:
                string[x], string[y] = string[y], string[x]
            case ['swap', str(x), str(y)]:
                i, j = string.index(x), string.index(y)
                string[i], string[j] = y, x
            case ['rotate', 'left' | 'right' as direction, int(x)]:
                shift = (x * (-1) ** (direction == 'right')) % size
                string[:] = string[-shift:] + string[:-shift]
            case ['rotate', str(x)]:
                current = string.index(x)
                loc = next(k for k in range(size) if (2*k + 1 + (k >= 4)) % size == current)
                shift = (loc - current) % size
                string[:] = string[-shift:] + string[:-shift]
            case ['reverse', int(x), int(y)]:
                string[x:y + 1] = string[y:x - 1 if x else None:-1]
            case ['move', int(x), int(y)]:
                string.insert(x, string.pop(y))
            case idk:
                raise ValueError(idk)
    return ''.join(string)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
