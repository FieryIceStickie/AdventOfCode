from operator import and_, lshift, or_, rshift
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    memory = {}
    data = {}
    for row in raw_data.read().splitlines():
        match row.split():
            case num, '->', var:
                try:
                    memory[var] = int(num)
                except ValueError:
                    data[var] = num
            case *args, '->', var:
                data[var] = args
    return memory, data


def part_a_solver(memory: dict[str, int], data: dict[str, list[str]]):
    def get_value(var: str):
        if var in memory:
            return memory[var]
        match data[var]:
            case arg1, op, arg2:
                operator = {'AND': and_, 'OR': or_, 'LSHIFT': lshift, 'RSHIFT': rshift}[op]
                try:
                    arg1 = int(arg1)
                except ValueError:
                    arg1 = get_value(arg1)
                try:
                    arg2 = int(arg2)
                except ValueError:
                    arg2 = get_value(arg2)
                value = operator(arg1, arg2)
            case 'NOT', arg:
                value = ~get_value(arg)
            case arg:
                value = get_value(arg)
        memory[var] = value
        return value

    return get_value('a')


def part_b_solver(memory: dict[str, int], data: dict[str, list[str]], a_signal: int):
    memory['b'] = a_signal

    def get_value(var: str):
        if var in memory:
            return memory[var]
        match data[var]:
            case arg1, op, arg2:
                operator = {'AND': and_, 'OR': or_, 'LSHIFT': lshift, 'RSHIFT': rshift}[op]
                try:
                    arg1 = int(arg1)
                except ValueError:
                    arg1 = get_value(arg1)
                try:
                    arg2 = int(arg2)
                except ValueError:
                    arg2 = get_value(arg2)
                value = operator(arg1, arg2)
            case 'NOT', arg:
                value = ~get_value(arg)
            case arg:
                value = get_value(arg)
        memory[var] = value
        return value

    return get_value('a')


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        memory, data = parser(file)

    print(res := part_a_solver(memory.copy(), data))
    print(part_b_solver(memory, data, res))
