from typing import TextIO

from Python.path_stuff import *


def parser(raw_data: TextIO) -> list[list[set[str], set[str]]]:
    parts = [line.split('|') for line in raw_data.read().splitlines()]
    return [[{*wins.split()[2:]}, {*hand.split()}] for wins, hand in parts]


def solver(data: list[list[set[str], set[str]]]) -> tuple[int, int]:
    cards = [1] * len(data)
    points = 0
    copies = 0
    for wins, hand in data:
        score = len(wins & hand)
        points += 1 << score >> 1
        copy_count, *cards = cards
        for i in range(score):
            cards[i] += copy_count
        copies += copy_count
    return points, copies


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(*solver(data))
