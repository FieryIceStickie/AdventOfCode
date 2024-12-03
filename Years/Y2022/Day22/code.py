import re
import time
from itertools import pairwise
from math import prod

from Years.Tools.utils import display_visited


def ctt(z: complex) -> tuple[int, int]:
    return int(z.real), int(z.imag)

def parser(filename: str):
    with open(filename, 'r') as file:
        flat_map, steps = file.read().split('\n\n')
        flat_dict = {x+y*1j: v=='#' for x, row in enumerate(flat_map.splitlines()) for y, v in enumerate(row) if v in '.#'}
        row_len, col_len = int(max(i.real for i in flat_dict))+1, int(max(i.imag for i in flat_dict))+1
        delta = row_len//(4 if row_len>col_len else 3)
        face_dicts = sorted((min(map(ctt, d)),d) for px, x in pairwise(range(0, row_len+1, delta))
                             for py, y in pairwise(range(0, col_len+1, delta))
                             if (d:={i: v for i, v in flat_dict.items() if px<=i.real<x and py<=i.imag<y}))
        instructions = tuple(int(i) if i.isdigit() else i for i in re.findall(r'\d+|[LR]', steps))
        # display_visited(set(), {i: '#' if v else '.' for m in face_dicts for i, v in m[1].items()}, ' ', True)
        return tuple((complex(*z), d) for z, d in face_dicts), instructions, delta, row_len, col_len

def part_a_solver(face_dicts: tuple[tuple[complex, dict[complex, bool]]],
                  instructions: list[str, int], delta: int, row_len: int, col_len: int):
    def get_adjacency(z: complex, dz: complex) -> int:
        while True:
            z += dz * delta
            z = complex(z.real % row_len, z.imag % col_len)
            for idx, (cz, _) in enumerate(face_dicts):
                if z == cz:
                    return idx
    adjacency_dicts = [{dz: get_adjacency(z, dz) for dz in (-1, 1j, 1, -1j)} for z, _ in face_dicts]
    current, current_face_dict = face_dicts[current_face := 0]
    facing = 1j
    for i in instructions:
        match i:
            case 'L':
                facing *= 1j
            case 'R':
                facing /= 1j
            case step:
                for _ in range(step):
                    z = current + facing
                    if z not in current_face_dict:
                        tentative_canon_rep, tentative_current_face_dict = \
                            face_dicts[tentative_current_face:=adjacency_dicts[current_face][facing]]
                        match facing:
                            case -1:
                                z = complex(tentative_canon_rep.real+delta-1, z.imag)
                            case 1j:
                                z = complex(z.real, tentative_canon_rep.imag)
                            case 1:
                                z = complex(tentative_canon_rep.real, z.imag)
                            case -1j:
                                z = complex(z.real, tentative_canon_rep.imag+delta-1)
                        if tentative_current_face_dict[z]:
                            break
                        canon_rep, current_face, current_face_dict = \
                            tentative_canon_rep, tentative_current_face, tentative_current_face_dict
                    if current_face_dict[z]:
                        break
                    current = z
    return int(sum(prod(i) for i in zip((1000, 4, 1), (current.real+1, current.imag+1, {1j:0,1:1,-1j:2,-1:3}[facing]))))


def part_b_solver(face_dicts: tuple[tuple[complex, dict[complex, bool]]],
                  instructions: list[str, int], delta: int, *_):
    delta -= 1
    #  01
    #  2
    # 34
    # 5
    adjacency_dicts = [
        {-1:(5, 1j),1j:(1, 1j),1:(2, 1),-1j:(3, 1j)},
        {-1:(5, -1),1j:(4, -1j),1:(2, -1j),-1j:(0, -1j)},
        {-1:(0, -1),1j:(1, -1),1:(4, 1),-1j:(3, 1)},
        {-1:(2, 1j),1j:(4, 1j),1:(5, 1),-1j:(0, 1j)},
        {-1:(2, -1),1j:(1, -1j),1:(5, -1j),-1j:(3, -1j)},
        {-1:(3, -1),1j:(4, -1),1:(1, 1),-1j:(0, 1)},
    ]
    # red, green, blue, yellow = tuple(f'\033[0;{i}m' for i in (31, 32, 34, 33))
    # color_dict = {-1: red, 1j: green, 1: blue, -1j: yellow}
    # print('\n'.join(''.join(f'{color_dict[c]}{t}' for t, c in v.values()) for i, v in enumerate(adjacency_dicts)))

    # Full     Red(-1)  Green(1j)  Blue(1)  Yellow(-1j)
    # 5123                51 3        2
    # 5420      5                              420
    # 0143      01                    43
    # 2450                24 0        5
    # 2153      2                              153
    # 3410      34                    10

    canon_rep, current_face_dict = face_dicts[current_face := 0]
    facing = 1j
    current = canon_rep
    # steps = {current: '>'}
    for i in instructions:
        match i:
            case 'L':
                facing *= 1j
            case 'R':
                facing /= 1j
            case step:
                for _ in range(step):
                    z = current + facing
                    if z not in current_face_dict:
                        tentative_current_face, tentative_facing = adjacency_dicts[current_face][facing]
                        tentative_canon_rep, tentative_current_face_dict = face_dicts[tentative_current_face]
                        d = current - canon_rep
                        match tentative_facing, facing:
                            case -1, -1:
                                d = complex(delta, d.imag)
                            case 1j, 1j:
                                d = d.real
                            case 1, 1:
                                d = 1j * d.imag
                            case -1j, -1j:
                                d = complex(d.real, delta)

                            case -1j, -1:
                                d = complex(delta-d.imag, delta)
                            case -1, 1j:
                                d = complex(delta,d.real)
                            case 1j, 1:
                                d = delta-d.imag
                            case 1, -1j:
                                d = 1j * d.real

                            case 1, -1:
                                d = 1j * delta-d.imag
                            case -1j, 1j:
                                d = complex(delta-d.real, delta)
                            case -1, 1:
                                d = complex(delta, delta-d.imag)
                            case 1j, -1j:
                                d = delta-d.real

                            case 1j, -1:
                                d = d.imag
                            case 1, 1j:
                                d = 1j * delta-d.real
                            case -1j, 1:
                                d = complex(d.imag, delta)
                            case -1, -1j:
                                d = complex(delta, delta-d.real)

                        # t\f  -1       1j       1      -1j
                        #  -1 (d,i)   (d,r)   (d,d-i) (d,d-r)
                        #  1j (i,0)   (r,0)   (d-i,0) (d-r,0)
                        #  1  (0,d-i) (0,d-r) (0,i)   (0,r)
                        # -1j (d-i,d) (d-r,d) (i,d)   (r,d)

                        # t\f     -1            1j             1           -1j
                        #  -1 (d,0)+(0,i)   (d,0)+(0,r)   (d,0)+(0,d-i) (d,0)+(0,d-r)
                        #  1j (0,0)+(i,0)   (0,0)+(r,0)   (0,0)+(d-i,0) (0,0)+(d-r,0)
                        #   1 (0,0)+(0,d-i) (0,0)+(0,d-r) (0,0)+(0,i)   (0,0)+(0,r)
                        # -1j (0,d)+(d-i,0) (0,d)+(d-r,0) (0,d)+(i,0)   (0,d)+(r,0)

                        # t -> -1: (d,0), 1j: (0,0), 1: (0,0), -1j: (0,d)
                        # f -> i, r, i, r
                        # t -> 1j, -1j, 1, -1
                        # 50*((t==-1)+1j*(t==-1j))+(2*(t.imag==0)-1)*(i if f.real else r)%50*{-1:1j,-1j:1}.get(t,t)for f in x for t in x




                        z = tentative_canon_rep + d
                        if tentative_current_face_dict[z]:
                            break
                        facing, canon_rep, current_face, current_face_dict = \
                            tentative_facing, tentative_canon_rep, tentative_current_face, tentative_current_face_dict
                    elif current_face_dict[z]:
                        break
                    current = z
                    # steps[current] = {-1: '^', 1j: '>', 1: 'v', -1j: '<'}[facing]
    return int(sum(prod(i) for i in zip((1000, 4, 1), (current.real+1, current.imag+1, {1j:0,1:1,-1j:2,-1:3}[facing]))))


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(*inputs))
    print(part_b_solver(*inputs))
