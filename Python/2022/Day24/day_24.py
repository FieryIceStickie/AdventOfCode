from collections import deque
from functools import cache
from itertools import count
from math import lcm


def parser(filename: str):
    with open(filename, 'r') as file:
        board = file.read().splitlines()
        row_len, col_len = len(board), len(board[0])
        start, end = 1j, complex(row_len-1, col_len-2)
        blizzards = [set(), set(), set(), set()]
        for x, row in enumerate(board):
            for y, v in enumerate(row):
                if 0 < x < row_len-1 and 0 < y < col_len - 1 and v != '.':
                    blizzards[{'^': 0, '>': 1, 'v': 2, '<': 3}[v]] |= {complex(x, y)}
        return blizzards, start, end, row_len, col_len


def l1(z: complex):
    return abs(z.real) + abs(z.imag)


def part_a_solver(blizzards: list[set[complex], ...], start: complex, end: complex, row_len: int, col_len: int):
    cycle_time = lcm(row_len - 2, col_len - 2)
    @cache
    def get_blizzards(t: int):
        if t == 0: return blizzards
        row_dict, col_dict = {0: row_len-2, row_len-1:1}, {0: col_len-2, col_len-1:1}
        return [
            {complex(row_dict.get(b.real-1, b.real-1),b.imag) for b in get_blizzards(t-1)[0]},
            {complex(b.real,col_dict.get(b.imag+1, b.imag+1)) for b in get_blizzards(t-1)[1]},
            {complex(row_dict.get(b.real+1, b.real+1),b.imag) for b in get_blizzards(t-1)[2]},
            {complex(b.real,col_dict.get(b.imag-1, b.imag-1)) for b in get_blizzards(t-1)[3]}
        ]

    def bfs(begin: complex, goal: complex) -> int:
        visited = {(0, begin)}
        active: deque[tuple[int, complex, tuple[complex, ...]]] = deque([(0, begin, (begin,))])
        while active:
            time, pos, path = active.popleft()
            board = get_blizzards(time)
            for d in (-1, 1j, 1, -1j, 0):
                if (z := pos + d) == goal:
                    return time
                elif z == begin or \
                        (0 < z.real < row_len - 1 and 0 < z.imag < col_len - 1 and all(z not in b for b in board)):
                    if ((time+1) % cycle_time, z) not in visited:
                        visited.add(((time+1)%cycle_time, z))
                        active.append((time+1, z, path + (z,)))
        else:
            raise ValueError

    def search(begin: complex, goal: complex) -> int:
        active = {begin}
        grid = get_blizzards(0)
        for t in count(1):
            new = set()
            for pos in active:
                for d in (1, 1j, -1, -1j, 0):
                    if (z := pos + d) == goal:
                        print(pos, d, goal)
                        return t
                    if z == begin or (0 < z.real < row_len - 1 and 0 < z.imag < col_len - 1
                                      and all(z not in b for b in grid)):
                        new.add(z)
            active = new
            grid = get_blizzards(t)
    print(search(start, end))
    return bfs(start, end)


def part_b_solver(blizzards: list[set[complex], ...], start: complex, end: complex, row_len: int, col_len: int):
    cycle_time = lcm(row_len - 2, col_len - 2)
    @cache
    def get_blizzards(t: int):
        nonlocal cycle_time
        if t == 0: return blizzards
        elif t > cycle_time: return get_blizzards(t % cycle_time)
        row_dict, col_dict = {0: row_len - 2, row_len - 1: 1}, {0: col_len - 2, col_len - 1: 1}
        return [
            {complex(row_dict.get(b.real - 1, b.real - 1), b.imag) for b in get_blizzards(t - 1)[0]},
            {complex(b.real, col_dict.get(b.imag + 1, b.imag + 1)) for b in get_blizzards(t - 1)[1]},
            {complex(row_dict.get(b.real + 1, b.real + 1), b.imag) for b in get_blizzards(t - 1)[2]},
            {complex(b.real, col_dict.get(b.imag - 1, b.imag - 1)) for b in get_blizzards(t - 1)[3]}
        ]

    def bfs(begin: complex, goal: complex, time: int) -> int:
        visited = {(time%cycle_time, begin)}
        active: deque[tuple[int, complex, tuple[complex, ...]]] = deque([(time, begin, (begin,))])
        while active:
            time, pos, path = active.popleft()
            board = get_blizzards(time)
            for d in (-1, 1j, 1, -1j, 0):
                if (z := pos + d) == goal:
                    return time
                elif z == begin or \
                        (0 < z.real < row_len - 1 and 0 < z.imag < col_len - 1 and all(z not in b for b in board)):
                    if ((time + 1) % cycle_time, z) not in visited:
                        visited.add(((time + 1) % cycle_time, z))
                        active.append((time + 1, z, path + (z,)))
        else:
            raise ValueError

    def search(begin: complex, goal: complex, time: int) -> int:
        active = {begin}
        grid = get_blizzards(time)
        for t in count(time + 1):
            new = set()
            for pos in active:
                for d in (1, 1j, -1, -1j, 0):
                    if (z := pos + d) == goal:
                        return t
                    if z not in new and (z == begin or (0 < z.real < row_len - 1 and 0 < z.imag < col_len - 1
                                      and all(z not in b for b in grid))):
                        new.add(z)
            active = new
            grid = get_blizzards(t)
    print(search(start, end, r:= search(end, start, s:=search(start, end, 0))))
    res = bfs(start, end, u:=bfs(end, start, v:=bfs(start, end, 0)))
    print(r, s, u, v)
    return res


if __name__ == '__main__':
    inputs = parser('day_24.txt')
    import time
    start = time.perf_counter()
    # print(part_a_solver(*inputs))
    print(part_b_solver(*inputs))
    end = time.perf_counter()
    print(end - start)
