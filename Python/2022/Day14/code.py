import time
from itertools import pairwise

from Python.Tools.utils import display_visited


def parser(filename: str):
    with open(filename, 'r') as file:
        rock_set = set()
        for path in file.read().splitlines():
            for node1, node2 in pairwise(path.split(' -> ')):
                node1 = complex(*(int(i) for i in node1.split(',')))
                node2 = complex(*(int(i) for i in node2.split(',')))
                if node1.real == node2.real:
                    start, end = sorted((int(node1.imag), int(node2.imag)))
                    rock_set |= {complex(node1.real, y) for y in range(start, end + 1)}
                elif node1.imag == node2.imag:
                    start, end = sorted((int(node1.real), int(node2.real)))
                    rock_set |= {complex(x, node1.imag) for x in range(start, end + 1)}
                else:
                    raise ValueError
        return rock_set


def pt1_move(block_set: set[complex], sand_pos: complex, abyss: float) -> bool:
    if sand_pos + 1j not in block_set:
        if sand_pos.imag == abyss:
            return False
        d = 1j
    elif sand_pos + -1+1j not in block_set:
        if sand_pos.imag == abyss:
            return False
        d = -1+1j
    elif sand_pos + 1+1j not in block_set:
        if sand_pos.imag == abyss:
            return False
        d = 1+1j
    else:
        block_set.add(sand_pos)
        return True
    return pt1_move(block_set, sand_pos + d, abyss)

def part_a_solver(block_set: set[complex]):
    rock_count = len(block_set)
    abyss = max(z.imag for z in block_set)
    while pt1_move(block_set, 500, abyss): pass
    return len(block_set) - rock_count

x = 0
def pt2_move(block_set: set[complex], sand_pos: complex):
    global x
    if sand_pos + 1j not in block_set:
        d = 1j
    elif sand_pos + -1+1j not in block_set:
        d = -1+1j
    elif sand_pos + 1+1j not in block_set:
        d = 1+1j
    else:
        block_set.add(sand_pos)
        if sand_pos == 500:
            return False
        return True
    return pt2_move(block_set, sand_pos + d)

def part_b_solver(block_set: set[complex]):
    global x
    width_set = {i.real for i in block_set}
    min_width, max_width = int(min(width_set)), int(max(width_set))
    floor = max(z.imag for z in block_set) + 2
    block_set |= {complex(x, floor) for x in range(min_width - 1000, max_width + 1001)}
    rock_count = len(block_set)
    while pt2_move(block_set, 500): pass
    return len(block_set) - rock_count


if __name__ == '__main__':
    # import cProfile
    # import pstats
    # with cProfile.Profile() as pr:
    start = time.perf_counter()
    inputs = parser('input.txt')
    print(part_a_solver(inputs.copy()))
    print(part_b_solver(inputs))
    end = time.perf_counter()
    print(end - start)
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.dump_stats(filename='../../Tools/profiling.prof')
