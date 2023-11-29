import numpy as np
from itertools import product
import networkx as nx
from collections import deque


def parser(filename: str):
    with open(filename, 'r') as file:
        return [tuple(map(int, i.split(','))) for i in file.read().splitlines()]


def part_a_solver(locs: list[tuple[int, int, int]]):
    existing = set()
    surfaces = 0
    deltas = [np.array(i) for i in ((0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0))]
    for x, y, z in locs:
        point = np.array((x, y, z))
        for d in deltas:
            if tuple(point+d) not in existing:
                surfaces += 1
            else:
                surfaces -= 1
        existing.add((x, y, z))
    return surfaces


def surround(x, y, z):
    return tuple(i for i in ((x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)) if
                 all(-2<x<22 for x in i))


def part_b_solver(locs: list[tuple[int, int, int]]):
    existing = set()
    surfaces = 0
    for x, y, z in locs:
        for d in surround(x, y, z):
            surfaces += 1 if d not in existing else -1
        existing.add((x, y, z))
    unvisited = deque([(0, 0, 0)])
    while unvisited:
        current = unvisited.pop()
        for d in surround(*current):
            if d not in existing:
                unvisited.append(d)
            existing.add(current)
    for x, y, z in {*product(range(20), range(20), range(20))}-existing:
        for d in surround(x, y, z):
            if d in existing:
                surfaces -= 1
    return surfaces


if __name__ == '__main__':
    inputs = parser('day_18.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
