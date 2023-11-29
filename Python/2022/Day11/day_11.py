from typing import Callable
import re
from collections import Counter
import numpy as np
from copy import deepcopy

def parser(filename: str):
    with open(filename, 'r') as file:
        return [[i[18:].split(', '),
                 get_op(*re.search(r'([*+]) (old|\d+)', o).groups()),
                 int(re.search(r'(\d+)', d).group(1)),
                 tuple(int(j) for j in re.findall(r'(\d+)', p1 + p2))]
                for _, i, o, d, p1, p2 in
                (line.split('\n') for line in file.read().split('\n\n'))]


def get_op(operator: str, operand: str) -> tuple[Callable[[np.ndarray], np.ndarray], int | None]:
    if operand == 'old':
        return np.square, None
    return {'+': np.add, '*': np.multiply}[operator], int(operand)

def part_a_solver(monkeys: list[list[list[int], tuple[int | None, Callable[[np.ndarray], np.ndarray]], int, tuple[int, int]]]):
    inspect_counter = Counter()
    for _ in range(20):
        for n, (items, (operator, operand), divisor, (t, f)) in enumerate(monkeys):
            tm, fm = monkeys[t], monkeys[f]
            items = np.array(items, dtype=int)
            inspect_counter[n] += items.size
            new_items = (operator(items) if operand is None else operator(items, operand)) // 3
            partition = new_items % divisor == 0
            tm[0] = tm[0] + new_items[partition].tolist()
            fm[0] = fm[0] + new_items[~partition].tolist()
            monkeys[n][0].clear()
    return np.prod(np.array(inspect_counter.most_common(2))[:, 1])


def part_b_solver(monkeys: list[list[list[int], tuple[int | None, Callable[[np.ndarray], np.ndarray]], int, tuple[int, int]]]):
    inspect_counter = Counter()
    lcm = np.lcm.reduce([d for _, _, d, _ in monkeys])
    for _ in range(10000):
        for n, (items, (operator, operand), divisor, (t, f)) in enumerate(monkeys):
            tm, fm = monkeys[t], monkeys[f]
            items = np.array(items, dtype=int)
            inspect_counter[n] += items.size
            new_items = (operator(items) if operand is None else operator(items, operand)) % lcm
            partition = new_items % divisor == 0
            tm[0] = tm[0] + new_items[partition].tolist()
            fm[0] = fm[0] + new_items[~partition].tolist()
            monkeys[n][0].clear()
    return np.prod(np.array(inspect_counter.most_common(2))[:, 1])


if __name__ == '__main__':
    import time
    # import cProfile
    # import pstats
    # with cProfile.Profile() as pr:
    start = time.perf_counter()
    inputs = parser('day_11.txt')
    print(part_a_solver(deepcopy(inputs)))
    print(part_b_solver(inputs))
    end = time.perf_counter()
    print(end - start)
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.dump_stats(filename='../../Tools/profiling.prof')
