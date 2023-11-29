from itertools import cycle
from functools import cache
from Tools.utils import display_visited, ctt
import numpy as np



def parser(filename: str):
    with open(filename, 'r') as file:
        return file.read()

def part_a_solver(moves):
    rocks = cycle(
        ((0, 1, 2, 3), (1j, 1 + 1j, 1 + 2j, 1, 2 + 1j), (0, 1, 2, 2 + 1j, 2 + 2j), (0, 1j, 2j, 3j), (0, 1, 1j, 1 + 1j)))
    piece_count = 0
    rock_set = {*range(-2, 6)}
    current_max = 0
    moves = cycle([1 if move == '>' else -1 for move in moves])
    @cache
    def start(r, a, b, c, d):
        for _, m in zip(range(4), (a, b, c, d)):
            if m == 1 and max(i.real for i in r) < 4:
                r = {i+1 for i in r}
            elif m == -1 and min(i.real for i in r) > -2:
                r = {i-1 for i in r}
        return r

    while piece_count < 2022:
        rock = {i + 1j*(current_max+1) for i in start(next(rocks), next(moves), next(moves), next(moves), next(moves))}
        while True:
            if any(i in rock_set for i in {i-1j for i in rock}):
                rock_set |= rock
                break
            rock = {i-1j for i in rock}
            move = next(moves)
            if move == 1 and max(i.real for i in rock) < 4 and not any(i in rock_set for i in {i+1 for i in rock}):
                rock = {i+1 for i in rock}
            elif move == -1 and min(i.real for i in rock) > -2 and not any(i in rock_set for i in {i-1 for i in rock}):
                rock = {i-1 for i in rock}
        piece_count += 1
        current_max = max(current_max, max(i.imag for i in rock))
    display_visited({i.conjugate() for i in rock_set})
    return int(max(i.imag for i in rock_set))


def display(board):
    for row in np.flip(board):
        for col in np.flip(row):
            print('#' if col else '.', end='')
        print('\n', end='')
    print('\n')


def part_b_solver(moves):
    board = np.zeros((7, 2000000), dtype=bool)
    board[:, 0] = True
    visited = {}
    move_count = len(moves)
    move_idx, rock_idx = 0, 0
    rocks = [np.array([*zip(*[ctt(j+2) for j in i])]) for i in
            ((0, 1, 2, 3), (1j, 1+1j, 1+2j, 1, 2+1j), (0, 1, 2, 2+1j, 2+2j), (0, 1j, 2j, 3j), (0, 1, 1j, 1+1j))]
    current_max = 0
    while True:
        if current_max > 50:
            upper_bit = tuple(tuple(i) for i in board[:,current_max-50:current_max+1])
            if upper_bit in visited:
                break
            visited[upper_bit] = (rock_idx, current_max)
        rock = rocks[rock_idx % 5].copy()
        rock[1] += current_max + 4
        while True:
            match moves[move_idx % move_count]:
                case '>':
                    temp_rock = rock.copy()
                    temp_rock[0] += 1
                    if np.amax(rock[0]) < 6 and not np.any(board[*temp_rock]):
                        rock = temp_rock
                case '<':
                    temp_rock = rock.copy()
                    temp_rock[0] -= 1
                    if np.amin(rock[0]) > 0 and not np.any(board[*temp_rock]):
                        rock = temp_rock
                case _:
                    pass
            move_idx += 1
            temp_rock = rock.copy()
            temp_rock[1] -= 1
            if np.any(board[*temp_rock]):
                board[*rock] = True
                current_max = max(current_max, np.amax(rock[1]))
                break
            rock = temp_rock
        rock_idx += 1
    prev_rock_idx, prev_max = visited[upper_bit]
    cycle_len, cycle_height = rock_idx - prev_rock_idx, current_max - prev_max
    new_height = current_max
    cycle_count, residue = divmod(1000000000000 - prev_rock_idx, cycle_len)
    piece_count = 0
    while piece_count < residue:
        rock = rocks[rock_idx % 5].copy()
        rock[1] += current_max + 4
        while True:
            drop_count = 0
            match moves[move_idx % move_count]:
                case '>':
                    temp_rock = rock.copy()
                    temp_rock[0] += 1
                    if np.amax(rock[0]) < 6 and not np.any(board[*temp_rock]):
                        rock = temp_rock
                case '<':
                    temp_rock = rock.copy()
                    temp_rock[0] -= 1
                    if np.amin(rock[0]) > 0 and not np.any(board[*temp_rock]):
                        rock = temp_rock
                case _:
                    pass
            move_idx += 1
            temp_rock = rock.copy()
            temp_rock[1] -= 1
            drop_count += 1
            if drop_count > 5:
                break
            if np.any(board[*temp_rock]):
                board[*rock] = True
                current_max = max(current_max, np.amax(rock[1]))
                break
            rock = temp_rock
        rock_idx += 1
        piece_count += 1
    return prev_max + cycle_count*cycle_height + current_max - new_height


if __name__ == '__main__':
    inputs = parser('day_17.txt')
    # print(part_a_solver(inputs))
    print(part_b_solver(inputs))
