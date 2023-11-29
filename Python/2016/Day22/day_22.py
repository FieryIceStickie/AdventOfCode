from typing import TextIO
import re
from itertools import islice, permutations
from typing import NamedTuple

from Python.path_stuff import *


class Node(NamedTuple):
    size: int
    used: int
    avail: int
    use_p: int


def parser(raw_data: TextIO):
    return {
        x + 1j*y: Node(size, used, avail, use_p)
        for x, y, size, used, avail, use_p in
        (map(int, re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%', row).groups())
         for row in islice(raw_data.read().splitlines(), 2, None))
    }


def part_a_solver(data: dict[complex, Node]):
    relevant = [(node.used, node.avail) for node in data.values()]
    return sum(1 for (used, _), (_, avail) in permutations(relevant, r=2) if used and used <= avail)


def part_b_solver(data: dict[complex, Node]):
    width, height = int(max(z.imag for z in data)) + 1, int(max(z.real for z in data)) + 1
    grid = {coord: ('G' if coord == height - 1
                    else '#' if node.size > 100
                    else '_' if not node.used
                    else '.')
            for coord, node in data.items()}
    for h in range(height):
        for w in range(width):
            print(grid[h+1j*w], end='')
        print()
    return


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day22/day_22.txt', 'r') as file:
        data = parser(file)

    # print(part_a_solver(data))
    print(part_b_solver(data))
