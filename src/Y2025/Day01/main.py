import math
from itertools import accumulate, pairwise
from typing import TextIO


def parser(raw_data: TextIO):
    return [
        (-1 if line.startswith("L") else 1) * int(line[1:])
        for line in raw_data.read().splitlines()
    ]


def full_solver(turns: list[int]):
    (*positions,) = accumulate(turns, initial=50)
    p1 = sum(not (p % 100) for p in positions)
    p2 = sum(
        (j // 100) - math.ceil(i / 100) + 1  #
        for i, j in map(sorted, pairwise(positions))
    )
    return p1, p2 - p1


if __name__ == "__main__":
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = "input.txt"
    else:
        path = test_path if testing else "input.txt"

    with open(path, "r") as file:
        data = parser(file)

    print(*full_solver(data))
