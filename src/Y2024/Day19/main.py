from typing import TextIO, Self
from attrs import define, field
from functools import cache

from Tools.Python.path_stuff import *
from Tools.Python.utils.utils import Res, res_sum


def parser(raw_data: TextIO):
    designs, towels = raw_data.read().split('\n\n')
    trie = Trie()
    for design in designs.split(', '):
        node = trie
        for s in design:
            node = node[s]
        node.marked = True
    return trie, towels.splitlines()


@define
class Trie:
    children: dict[str, Self] = field(factory=dict)
    marked: bool = False

    def __getitem__(self, key):
        if key in self.children:
            return self.children[key]
        self.children[key] = Trie()
        return self.children[key]


def check(designs: Trie, towel: str):
    tl = len(towel)

    @cache
    def solve(idx: int):
        if idx == tl:
            return 1
        node = designs
        count = 0
        for i in range(idx, tl):
            s = towel[i]
            if s not in node.children:
                break
            node = node.children[s]
            if node.marked:
                count += solve(i + 1)
        return count
    return solve(0)


def full_solver(designs: Trie, towels: list[str]):
    return res_sum(
        Res(1, res) for towel in towels
        if (res := check(designs, towel))
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(*data))
