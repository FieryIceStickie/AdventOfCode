from typing import TextIO, Iterator

from path_stuff import *
import re
from itertools import combinations, chain
import heapq
from functools import lru_cache


def parser(raw_data: TextIO):
    elements = {}
    c = 1
    floors = []
    floor_pattern = re.compile(r'(\w+)(?:-compatible)? (generator|microchip)')
    for row in raw_data.read().splitlines():
        items = set()
        floors.append(items)
        for element, obj_type in floor_pattern.findall(row):
            if element in elements:
                num = elements[element]
            else:
                elements[element] = num = c
                c += 1
            items |= {num*(-1)**(obj_type == 'generator')}
    return [frozenset(floor) for floor in floors], c


@lru_cache(maxsize=300)
def validate(floor: frozenset[int]) -> bool:
    return all(item > 0 for item in floor) or all(-item in floor for item in floor if item > 0)


def get_neighbours(level: int,
                   floors: tuple[frozenset[int]],
                   max_level: int) -> Iterator[tuple[int, tuple[frozenset[int]]]]:
    floor = floors[level]
    for items in chain(combinations(floor, 2), [(i,) for i in floor]):
        if not validate(orig_floor := floor - {*items}):
            continue
        for d in (-1, 1):
            new_level = level + d
            if 0 <= new_level < max_level:
                new_floor = floors[new_level] | {*items}
                if not validate(new_floor):
                    continue
                yield (new_level, tuple(
                    orig_floor if i == level
                    else new_floor if i == new_level
                    else v for i, v in enumerate(floors)
                ))


def heuristic(state: list[frozenset[int]], max_level: int) -> int:
    return sum(i * len(v) for i, v in enumerate(state[1][max_level - 2::-1], start=1))


def hash_state(level: int, floors: list[frozenset]) -> int:
    seen = {}
    regularized = []
    c = 1
    for floor in floors:
        new_floor = set()
        for item in floor:
            m = abs(item)
            if m not in seen:
                seen[m] = c
                c += 1
            new_floor.add((-1) ** (item < 0) * seen[m])
        regularized.append(frozenset(new_floor))
    return hash((level, tuple(regularized)))


def a_star(floors: tuple[frozenset]) -> int:
    max_level = len(floors)
    current = hash_state(0, floors)
    active = [(0, (0, floors))]
    heapq.heapify(active)
    visited = {current: 0}
    while active:
        _, (level, floors) = heapq.heappop(active)
        if not any(floors[:-1]):
            break
        g = visited[hash_state(level, floors)] + 1
        for new_state in get_neighbours(level, floors, max_level):
            state_hash = hash_state(*new_state)
            if visited.get(state_hash, float('inf')) > g:
                visited[state_hash] = g
                heapq.heappush(active, (g + heuristic(new_state, max_level), new_state))
    else:
        return None
    return visited[hash_state(level, floors)]


def part_a_solver(floors: list[frozenset]):
    return a_star(tuple(floors))


def part_b_solver(floors: list[frozenset], c: int):
    floors[0] |= {c, c+1, -c, -c-1}
    return a_star(tuple(floors))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 11/day_11.txt', 'r') as file:
        data, c = parser(file)
    # print(part_a_solver(data))
    print(part_b_solver(data, c))
