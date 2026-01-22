from collections.abc import Iterable, Sequence
from math import prod
from typing import TextIO

from rich.pretty import pprint


def parser(raw_data: TextIO) -> Sequence[tuple[Iterable[int], int]]:
    return [
        (map(int, coefs), prod(map(int, res[:-1].split("x"))))
        for res, *coefs in (
            line.split(" ")  #
            for line in raw_data.read().split("\n\n")[-1].splitlines()
        )
    ]


def full_solver(eqns: Sequence[tuple[Iterable[int], int]]) -> int:
    return sum(9 * sum(coefs) <= res for coefs, res in eqns)


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

    pprint(full_solver(data))
