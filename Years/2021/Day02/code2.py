from typing import Any

from Years.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return file.read().splitlines()
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            return file.read().splitlines()
    return inputs


def solver(inputs: Any) -> Any:
    x = 0
    y = 0
    aim = 0
    for i in inputs:
        direction, magnitude = i.split()
        magnitude = int(magnitude)
        match direction:
            case 'forward':
                x += magnitude
                y += magnitude * aim
            case 'down':
                aim += magnitude
            case 'up':
                aim -= magnitude
    return x * y


def display(product) -> None:
    print(product)


if __name__ == '__main__':
    answer = solver(parser(
        'forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2',
        file_name='input.txt',
        testing=False))
    display(answer)
