from functools import reduce
from itertools import product
from operator import xor
from typing import TextIO

from attrs import frozen
from rich.pretty import pprint
from z3 import Int, Optimize, sat

@frozen
class Machine:
    config: int
    buttons: list[set[int]]
    joltages: list[int]

    @classmethod
    def parse(cls, line: str):
        config, *buttons, joltages = line.split(" ")
        return cls(
            sum(1 << i for i, v in enumerate(config[1:-1]) if v == "#"),
            [{*map(int, button[1:-1].split(","))} for button in buttons],
            [*map(int, joltages[1:-1].split(","))],
        )


def parser(raw_data: TextIO) -> list[Machine]:
    return [Machine.parse(line) for line in raw_data.read().splitlines()]


def full_solver(machines: list[Machine]) -> tuple[int, int]:
    p1 = p2 = 0
    for machine in machines:
        button_bits = [sum(1 << i for i in button) for button in machine.buttons]
        p1 += min(
            sum(indices)
            for indices in product(range(2), repeat=len(button_bits))
            if not reduce(
                xor,
                (button_bits[i] for i, v in enumerate(indices) if v),
                initial=machine.config,
            )
        )
        s = Optimize()
        for idx, joltage in enumerate(machine.joltages):
            s.add(
                sum(
                    Int(f"x{i}")
                    for i, button in enumerate(machine.buttons)
                    if idx in button
                )
                == joltage
            )
        for i in range(len(machine.buttons)):
            s.add(Int(f"x{i}") >= 0)
        h = s.minimize(sum(Int(f"x{i}") for i in range(len(machine.buttons))))
        if s.check() == sat:
            p2 += s.lower(h).as_long()
        else:
            raise ValueError("joever")

    return (p1, p2)


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
