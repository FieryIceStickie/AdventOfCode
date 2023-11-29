import re
from typing import Any


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = 'test.txt'
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        x1, x2, y1, y2 = re.match(r'target area: x=([-\d]+)\.\.([-\d]+), y=([-\d]+)\.\.([-\d]+)',
                                  file.read().rstrip()).groups()
        return max(abs(int(y1)), abs(int(y2)))


def solver(y_max: int) -> Any:
    return y_max * (y_max - 1) // 2


def display(max_y) -> None:
    print(max_y)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='day_17.txt',
        testing=False))
    display(answer)
