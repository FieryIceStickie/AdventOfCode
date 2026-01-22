import re
from typing import TextIO

type Intervals = list[tuple[int, int]]
type Cupcakes = list[int]


def parser(raw_data: TextIO) -> tuple[Intervals, Cupcakes]:
    intervals, cupcakes = raw_data.read().split("\n\n")
    return (
        [(int(s), int(e)) for s, e in re.findall(r"(\d+)-(\d+)", intervals)],
        [*map(int, cupcakes.splitlines())],
    )


def merge_intervals(intervals: Intervals) -> Intervals:
    it = iter(intervals)
    start, end = next(it)
    rtn: Intervals = []
    for s, e in it:
        if end + 1 < s:
            rtn.append((start, end))
            start, end = s, e
        elif end < e:
            end = e
    rtn.append((start, end))
    return rtn


def p1_solve(intervals: Intervals, cupcakes: Cupcakes) -> int:
    p1 = 0
    it = iter(intervals)
    start, end = next(it)
    for cupcake in cupcakes:
        while end < cupcake:
            if interval := next(it, None):
                start, end = interval
            else:
                return p1
        p1 += start <= cupcake
    return p1


def full_solver(intervals: Intervals, cupcakes: Cupcakes) -> tuple[int, int]:
    intervals.sort()
    cupcakes.sort()
    intervals = merge_intervals(intervals)
    return p1_solve(intervals, cupcakes), sum(e - s + 1 for s, e in intervals)


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

    print(*full_solver(*data))
