import re
from collections.abc import Iterable
from itertools import groupby
from math import prod
from typing import TextIO
import time


def parser(raw_data: TextIO) -> list[str]:
    return raw_data.read().splitlines()


def solver(cols: Iterable[Iterable[int]], ops: Iterable[str]) -> int:
    return sum((sum if op == "+" else prod)(nums) for nums, op in zip(cols, ops))


def full_solver(lines: list[str]) -> tuple[int, int]:
    *rows, ops = lines
    ops = re.findall(r"[+*]", ops)
    p1_cols = zip(*(map(int, re.findall(r"\d+", line)) for line in rows))
    p2_cols = (
        map(int, g)
        for k, g in groupby(map("".join, zip(*rows)), key=lambda s: bool(s.strip()))
        if k
    )
    return solver(p1_cols, ops), solver(p2_cols, ops)


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
