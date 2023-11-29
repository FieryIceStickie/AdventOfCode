from typing import TextIO
from math import factorial

from Python.Tools.utils import try_int

from Python.path_stuff import *


def parser(raw_data: TextIO):
    return [[*map(try_int, row.split())] for row in raw_data.read().splitlines()]


def sim(data: list[list[str, int]], memory: dict[str, int]) -> dict[str, int]:
    program_counter = 0
    end = len(data)
    while program_counter < end:
        instruction = data[program_counter]
        program_counter += 1
        match instruction:
            case 'cpy', x, str(y):
                memory[y] = memory.get(x, x)
            case 'inc', str(x):
                memory[x] += 1
            case 'dec', str(x):
                memory[x] -= 1
            case 'jnz', x, y:
                if memory.get(x, x):
                    program_counter += memory.get(y, y) - 1
            case 'tgl', str(x):
                pointer = program_counter + memory[x] - 1
                if pointer < 0 or pointer >= end:
                    continue
                opcode, *operands = data[pointer]
                if len(operands) == 2:
                    data[pointer] = ['cpy' if opcode == 'jnz' else 'jnz', *operands]
                elif len(operands) == 1:
                    data[pointer] = ['dec' if opcode == 'inc' else 'inc', *operands]
                else:
                    raise ValueError
            case _:
                pass
    return memory


def solve(data: list[list[str, int]], start: int):
    (_, x, _), (_, y, _) = data[19:21]
    return factorial(start) + x*y


def part_a_solver(data: list[list[str, int]]):
    return solve(data, 7)


def part_b_solver(data: list[list[str, int]]):
    return solve(data, 12)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day23/day_23.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data.copy()))
    print(part_b_solver(data.copy()))
