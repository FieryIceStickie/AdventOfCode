from Years.Tools.utils import display_visited


def ctt(c: complex) -> tuple[int, int]:
    return int(c.real), int(c.imag)


def sgn(x: float) -> -1 | 0 | 1:
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def surround(c: complex, *, diagonal: bool = True, inclusive: bool = True) -> list[complex]:
    if diagonal:
        delta = [-1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1, -1-1j]
    else:
        delta = [-1j, 1, 1j, -1]
    return [c + d for d in delta] + ([c] if inclusive else [])


def parser(filename: str):
    with open(filename, 'r') as file:
        moves = []
        for i in file.read().splitlines():
            move, steps = i.split()
            moves.append((move_dict[move], int(steps)))
        return moves


move_dict: dict[str | complex, str | complex] = {'U': -1j, 'R': 1, 'D': 1j, 'L': -1}
move_dict = {**move_dict, **{v: i for i, v in move_dict.items()}}

def part_a_solver(moves: list[tuple[complex, int]]):
    visited = {0}
    head_pos = 0
    tail_pos = 0
    surroundings = surround(0)
    for move, step in moves:
        for _ in range(step):
            head_pos += move
            delta = head_pos - tail_pos
            if delta not in surroundings:
                tail_pos += complex(sgn(delta.real), sgn(delta.imag))
                visited.add(tail_pos)
    return len(visited)


def part_b_solver(moves: list[tuple[complex, int]]):
    visited = {0}
    knot_pos = [0] * 10
    surroundings = surround(0)
    for move, step in moves:
        for _ in range(step):
            knot_pos[0] += move
            for i in range(9):
                delta = knot_pos[i] - knot_pos[i + 1]
                if delta in surroundings:
                    break
                knot_pos[i + 1] += complex(sgn(delta.real), sgn(delta.imag))
            else:
                visited.add(knot_pos[-1])
        # display_visited(visited, {v: str(i) for i, v in reversed([*enumerate(knot_pos)])})
    return len(visited)


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
