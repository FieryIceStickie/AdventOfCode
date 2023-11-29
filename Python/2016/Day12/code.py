from typing import TextIO

from Python.path_stuff import *


def conv_int(data: str) -> int | str:
    try:
        return int(data)
    except ValueError:
        return data


def parser(raw_data: TextIO):
    return [[*map(conv_int, row.split())] for row in raw_data.read().splitlines()]


def sim(data: list[list[str, int]], memory: dict[str, int]) -> dict[str, int]:
    program_counter = 0
    end = len(data)
    while program_counter < end:
        instruction = data[program_counter]
        program_counter += 1
        match instruction:
            case 'cpy', int(x), y:
                memory[y] = x
            case 'cpy', str(x), y:
                memory[y] = memory[x]
            case 'inc', x:
                memory[x] += 1
            case 'dec', x:
                memory[x] -= 1
            case 'jnz', x, y:
                if memory.get(x, x):
                    program_counter += y - 1
            case idk:
                print(idk)
                raise ValueError
    return memory


def solve(data: list[list[str, int]], c: bool):
    (_, x, _), (_, y, _) = data[16:18]
    return (9227465 if c else 317811) + x*y


def part_a_solver(data: list[list[str, int]]):
    return solve(data, False)


def part_b_solver(data: list[list[str, int]]):
    return solve(data, True)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
