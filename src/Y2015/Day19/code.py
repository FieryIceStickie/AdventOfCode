import re
from collections import defaultdict
from itertools import count, pairwise
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    conversion_text, seed_text = raw_data.read().split('\n\n')
    conversions = defaultdict(list)
    seed = re.findall(r'[A-Z][a-z]*', seed_text)
    electrons = []
    for line in conversion_text.split('\n'):
        key, value = line.split(' => ')
        (electrons if key == 'e' else conversions[key]).append(re.findall(r'[A-Z][a-z]*', value))
    return conversions, seed, electrons


def part_a_solver(conversions: defaultdict[str, list[str]], seed: list[str], electrons: list[list[str]]):
    return len({hash((*seed[:idx], *value, *seed[idx+1:]))
                for key, values in conversions.items()
                for idx, v in enumerate(seed) if v == key
                for value in values})


def bfs(seed: list[str],
        targets: dict[tuple[int, int], int],
        simple_convs: dict[tuple[int, int], int]) -> tuple[int, int]:
    # print('a', seed, targets, simple_convs)
    current = {tuple(seed)}
    for t in count(1):
        # print(current)
        intersection = targets.keys() & current
        if intersection:
            if len(intersection) > 1:
                print(intersection, seed, current)
                raise ValueError()
            return t, targets[intersection.pop()]

        current = {
            (*node[:idx], product, *node[idx+2:])
            for node in current
            for reactants, product in simple_convs.items()
            for idx, tentative_reactants in enumerate(pairwise(node))
            if reactants == tentative_reactants
        }
        if not current:
            raise ValueError('no break')


def part_b_solver(conversions: defaultdict[str, list[str]], seed: list[str], electrons: list[list[str]]):
    simple_convs, struct_convs = {}, defaultdict(dict)
    for key, values in conversions.items():
        for value in values:
            match value:
                case [pre_elem, 'Rn', *filling, 'Ar']:
                    struct_convs[pre_elem][*filling] = key
                case _:
                    simple_convs[*value] = key
    stack = [[seed[0]]]
    step_count = 0

    for key, value in struct_convs.items():
        print(key)
        print(value, '\n')

    return

    for prev, curr in pairwise(seed):
        print(prev, curr, [''.join(i) for i in stack])
        if curr == 'Rn':
            print('start')
            prev_elem = stack[-1].pop()
            if prev_elem not in struct_convs:
                prev_prev_elem = stack[-1].pop()
                prev_elem = simple_convs[prev_prev_elem, prev_elem]
            stack.append([prev_elem])
        elif curr == 'Ar':
            print('end')
            key, *filling = stack.pop()
            steps, res = bfs(filling, struct_convs[key], simple_convs)
            step_count += steps
            stack[-1].append(res)
        else:
            print('normal')
            stack[-1].append(curr)
    return step_count


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(*data))
    print(part_b_solver(*data))
