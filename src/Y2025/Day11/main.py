from functools import cache
from typing import TextIO

from rich.pretty import pprint

type Graph = dict[str, set[str]]


def parser(raw_data: TextIO) -> Graph:
    return {
        u: {*vs.split(" ")}
        for u, _, vs in (line.partition(": ") for line in raw_data.read().splitlines())
    }


def full_solver(graph: Graph) -> tuple[int, int]:
    @cache
    def num_paths(u: str, v: str) -> int:
        return 1 if u == v else sum(num_paths(w, v) for w in graph.get(u, ()))

    a, b = "dac", "fft"
    if not num_paths(a, b):
        a, b = b, a
    return (num_paths("you", 'out'), num_paths('svr', a) * num_paths(a, b) * num_paths(b, 'out'))


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
