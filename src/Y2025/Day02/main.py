import re
from typing import TextIO


def parser(raw_data: TextIO) -> list[tuple[int, int]]:
    return [
        tuple(map(int, interval))  # pyright: ignore[reportAny, reportReturnType]
        for interval in re.findall(r"(\d+)-(\d+)", raw_data.read()) # pyright: ignore[reportAny]
    ]

def full_solver(ranges: list[tuple[int, int]]):
    return sum(
        n 
        for a, b in ranges
        for n in range(a, b+1)
        if re.match(r'^(\d+)\1$', str(n))
    ), sum(
        n 
        for a, b in ranges
        for n in range(a, b+1)
        if re.match(r'^(\d+)\1+$', str(n))
    )


if __name__ == "__main__":
    testing = False

    path = "test.txt" if testing else "input.txt"

    with open(path, "r") as file:
        data = parser(file)

    print(*full_solver(data))
