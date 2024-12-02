from collections import Counter
from typing import Any

from Tools.Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = test_path
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        lines = file.read().splitlines()
        polymer = lines[0]
        insertion_dict = {i: v for i, v in (j.split(' -> ') for j in lines[2:])}
        return polymer, insertion_dict


def polymerization(polymer: str, insertion_dict: dict):
    while True:
        new_polymer = ''
        insertions = tuple(insertion_dict.get(polymer[i:i+2], None) for i, v in enumerate(polymer[:-1])) + (None,)
        for i, j in zip(polymer, insertions):
            if j is None:
                new_polymer += i
            else:
                new_polymer += i + j
        yield new_polymer
        polymer = new_polymer


def solver(polymer: str, insertion_dict: dict) -> Any:
    polymer_sim = polymerization(polymer, insertion_dict)
    for _ in range(10):
        polymer = next(polymer_sim)
    polymer_count = Counter(polymer)
    counts = polymer_count.most_common()
    return counts[0][1] - counts[-1][1]


def display(subtraction) -> None:
    print(subtraction)


if __name__ == '__main__':
    answer = solver(*parser(
        file_name='input.txt',
        testing=True))
    display(answer)
