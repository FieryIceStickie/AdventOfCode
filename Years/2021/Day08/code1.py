from typing import Any

import numpy as np

from Years.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            signals, outputs = [], []
            for line in lines:
                signal, output = line.split(' | ')
                signals.append(signal.split())
                outputs.append(output.split())
            return np.array(signals), np.array(outputs)
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            lines = file.read().splitlines()
            signals, outputs = [], []
            for line in lines:
                signal, output = line.split(' | ')
                signals.append(signal.split())
                outputs.append(output.split())
            return np.array(signals), np.array(outputs)
    return inputs


def solver(inputs: Any) -> Any:
    signals, outputs = inputs
    count = 0
    for i in outputs:
        for output in i:
            if len(output) in (2, 3, 4, 7):
                count += 1
    return count


def display(count) -> None:
    print(count)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
