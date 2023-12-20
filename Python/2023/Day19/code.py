from typing import TextIO, NamedTuple
from collections.abc import Callable

from Python.path_stuff import *
import re
from bisect import bisect
from itertools import starmap
from operator import lt, gt

from math import prod
from operator import attrgetter
from attrs import evolve, frozen



class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

def compare(category: str, is_inc: bool, num: int, result: str) -> Callable[[Part], str | None]:
    return lambda part: result if [lt, gt][is_inc](getattr(part, category), num) else None


def parser(raw_data: TextIO):
    workflows, ratings = raw_data.read().split('\n\n')
    parts = [Part(*map(int, re.findall(r'\d+', line))) for line in ratings.splitlines()]
    workflow_dict = {}
    for line in workflows.splitlines():
        name, rules = re.match(r'(\w+){(.+)}', line).groups()
        *patterns, default = rules.split(',')
        workflow_dict[name] = [
            [(category, op == '>', int(num), res)
             for category, op, num, res in (re.match(r'([xmas])([<>])(\d+):(\w+)', rule).groups() for rule in patterns)],
            default,
        ]
    return workflow_dict, parts


def part_a_solver(workflows: dict[str, list[list[tuple[str, bool, int, str]], bool]], parts: list[Part]):
    workflows = {
        name: [[*starmap(compare, patterns)], default]
        for (name, (patterns, default)) in workflows.items()
    }

    def check(part: Part, workflow: str = 'in') -> bool:
        patterns, default = workflows[workflow]
        for pattern in patterns:
            if result := pattern(part):
                if result in ('A', 'R'):
                    return result == 'A'
                return check(part, result)
        if default in ('A', 'R'):
            return default == 'A'
        return check(part, default)

    return sum(
        sum(part)
        for part in parts
        if check(part)
    )

@frozen
class Range:
    start: int
    end: int
    def __len__(self):
        return self.end - self.start + 1
    def __and__(self, other):
        if self.end < other.start or self.start > other.end:
            return None
        return Range(max(self.start, other.start), min(self.end, other.end))
    def __repr__(self):
        return f'{self.start}->{self.end}'

@frozen
class RangePart:
    x: Range
    m: Range
    a: Range
    s: Range



def part_b_solver(workflows: dict[str, list[list[tuple[str, bool, int, str]], bool]], _):
    def count(part: RangePart, workflow: str = 'in') -> int:
        if workflow == 'A':
            return prod(map(len, attrgetter(*'xmas')(part)))
        elif workflow == 'R':
            return 0

        patterns, default = workflows[workflow]
        rtn = 0
        for category, is_inc, num, res in patterns:
            crange = getattr(part, category)
            if is_inc:
                reject, accept = Range(1, num), Range(num+1, 4000)
            else:
                accept, reject = Range(1, num-1), Range(num, 4000)
            reject &= crange
            accept &= crange
            if accept:
                rtn += count(evolve(part, **{category: accept}), res)
            if reject:
                part = evolve(part, **{category: reject})
        rtn += count(part, default)
        return rtn
    return count(RangePart(*[Range(1, 4000)]*4))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(*data))
    print(part_b_solver(*data))
