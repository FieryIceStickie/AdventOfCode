from itertools import pairwise
from typing import TextIO

from Tools.Python.path_stuff import *
from functools import cmp_to_key


def parser(raw_data: TextIO):
    rules_str, updates_str = raw_data.read().split('\n\n')
    rules = {
        tuple(map(int, rule.split('|')))
        for rule in rules_str.split('\n')
    }
    updates = [
        [*map(int, line.split(','))]
        for line in updates_str.split('\n')
    ]
    return rules, updates


def full_solver(rules: set[tuple[int, int]], updates: list[list[int]]):
    p1 = p2 = 0

    def cmp(n: int, m: int) -> int:
        return 1 if (n, m) in rules else -1

    for update in updates:
        if all(
            (n, m) in rules
            for n, m in pairwise(update)
        ):
            p1 += update[len(update) // 2]
        else:
            update.sort(key=cmp_to_key(cmp))
            p2 += update[len(update) // 2]
    return p1, p2


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(*data))