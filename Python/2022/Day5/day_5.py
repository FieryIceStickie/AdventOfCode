import re
from collections import defaultdict
from itertools import repeat
from typing import NamedTuple
from copy import deepcopy


class Move(NamedTuple):
    count: int
    start: int
    end: int

    @classmethod
    def from_str(cls, *args: str):
        return cls(*(int(i) for i in args))


def parser(filename: str):
    with open(filename, 'r') as file:
        crates, moves = file.read().split('\n\n')

        stacks = defaultdict(list)
        for row in crates.split('\n')[-2::-1]:
            for i, v in enumerate(row[1::4]):
                if v != ' ':
                    stacks[i+1].append(v)

        moves = [Move.from_str(*re.match(r'move (\d+) from (\d+) to (\d+)', row).groups()) for row in moves.split('\n')]

        return stacks, moves


def display(stacks: dict[int, list[str]]):
    for i, v in stacks.items():
        print(f'{i} {"".join(v)}')


def part_a_solver(stacks: dict[int, list[str]], moves: list[Move]) -> str:
    for count, start, end in moves:
        for _ in repeat(None, count):
            stacks[end].append(stacks[start].pop())
    return ''.join(i[-1] for i in stacks.values())


def part_b_solver(stacks: dict[int, list[str]], moves: list[Move]) -> str:
    for count, start, end in moves:
        stacks[end].extend(stacks[start][-count:])
        stacks[start] = stacks[start][:-count]
    return ''.join(i[-1] for i in stacks.values())


if __name__ == '__main__':
    inputs = parser('day_5.txt')
    print(part_a_solver(*deepcopy(inputs)))
    print(part_b_solver(*inputs))
