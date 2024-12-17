from typing import TextIO
import re
from itertools import batched

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    return [*map(int, re.findall(r'\d+', raw_data.read()))]


def sim(reg: list[int], program: list[int]) -> list[int]:
    pt = 0
    out = []

    def get_combo(n: int) -> int:
        if n < 4:
            return n
        return reg[n - 4]

    while pt + 1 < len(program):
        o = program[pt + 1]
        match program[pt]:
            case 0:
                reg[0] >>= get_combo(o)
            case 1:
                reg[1] ^= o
            case 2:
                reg[1] = get_combo(o) % 8
            case 3:
                if reg[0]:
                    pt = o
                    continue
            case 4:
                reg[1] ^= reg[2]
            case 5:
                out.append(get_combo(o) % 8)
            case 6:
                reg[1] = reg[0] >> get_combo(o)
            case 7:
                reg[2] = reg[0] >> get_combo(o)
        pt += 2
    return out


def full_solver(data: list[int]):
    a, _, _, *program = data
    v, w = [n for c, n in batched(program, 2) if c == 1]
    vw = v ^ w

    def f(a: int, r: int) -> int:
        return (r ^ vw ^ a >> (r ^ v)) & 7

    out = []
    while a:
        q, r = divmod(a, 8)
        out.append(f(a, r))
        a = q

    def solve(num: int, target: int) -> int | None:
        if target == len(program):
            return num
        for r in range(8):
            if not target and not r:
                continue
            if f(a := num << 3 | r, r) == program[~target]:
                if res := solve(a, target + 1):
                    return res
        return 0

    return ','.join(map(str, out)), solve(0, 0)


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*full_solver(data))
