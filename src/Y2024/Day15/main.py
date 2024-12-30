from itertools import count
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    grid_str, move_str = raw_data.read().split('\n\n')
    boxes = set()
    grid = set()
    bot = None
    for x, row in enumerate(grid_str.splitlines()):
        for y, v in enumerate(row):
            z = x + 1j * y
            if v == '#':
                grid.add(z)
            elif v == 'O':
                boxes.add(z)
            elif v == '@':
                bot = z
    faces = dict(zip('^>v<', (-1, 1j, 1, -1j)))
    moves = [
        faces[m]
        for m in move_str
        if m != '\n'
    ]
    return grid, boxes, moves, bot


def part_a_solver(grid: set[complex], boxes: set[complex], moves: list[complex], z: complex):
    grid = grid.copy()
    boxes = boxes.copy()

    for m in moves:
        z += m
        can_move = z not in grid
        if z in boxes and (can_move := (b := next(b for n in count(1) if (b := z + n * m) not in boxes)) not in grid):
            boxes ^= {z, b}
        elif not can_move:
            z -= m
    return p1_disp(grid, boxes, z), sum(
        int(100 * z.real + z.imag)
        for z in boxes
    )


def part_b_solver(grid: set[complex], boxes: set[complex], moves: list[complex], z: complex):
    grid = {z + d for z in grid for d in (0, 1j / 2)}
    boxes = boxes.copy()

    def push(box: complex, d: complex) -> bool:
        return (box in pushing or pushing.add(box)
                or not {box + d, box + d + 1j / 2} & grid
                and all(push(b, d) for b in (
                    [box + 2 * d] if d.imag else
                    [box + d + dy for dy in (-1j / 2, 0, 1j / 2)]
                ) if b in boxes))

    for i, m in enumerate(m / 2 if m.imag else m for m in moves):
        z += m
        can_move = z not in grid
        pushing = set()
        if (s := {z, z - 1j / 2} & boxes) and (can_move := push(s.pop(), m)):
            boxes ^= pushing ^ {b + m for b in pushing}
        elif not can_move:
            z -= m
    return p2_disp(grid, boxes, z), sum(
        int(100 * z.real + 2 * z.imag)
        for z in boxes
    )


def p1_disp(grid: set[complex], boxes: set[complex], bot: complex) -> str:
    return '\n'.join(
        ''.join(
            '#' if (z := x + 1j * y) in grid else
            'O' if z in boxes else
            '@' if bot == z else
            '.'
            for y in range(int(max(z.imag for z in grid)) + 1)
        ) for x in range(int(max(z.real for z in grid)) + 1)
    )


def p2_disp(grid: set[complex], boxes: set[complex], bot: complex) -> str:
    return '\n'.join(
        ''.join(
            '#' if (z := x + 1j * y + d) in grid else
            '[' if z in boxes else
            ']' if z - 1j / 2 in boxes else
            '@' if bot == z else
            '.'
            for y in range(int(max(z.imag for z in grid)) + 1)
            for d in (0, 1j / 2)
        ) for x in range(int(max(z.real for z in grid)) + 1)
    )


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    p1_disp, p1 = part_a_solver(*data)
    p2_disp, p2 = part_b_solver(*data)
    # print(p1_disp, end='\n\n')
    # print(p2_disp)
    print(p1, p2)
