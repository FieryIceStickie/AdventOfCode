from collections import Counter
from typing import Any

import numpy as np

from Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            signals, outputs = [], []
            for line in lines:
                signal, output = line.split(' | ')
                signals.append(signal.split())
                outputs.append(output.split())
            return signals, outputs
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            lines = file.read().splitlines()
            signals, outputs = [], []
            for line in lines:
                signal, output = line.split(' | ')
                signals.append(signal.split())
                outputs.append(output.split())
            return signals, outputs
    return inputs


def solver(inputs: Any) -> Any:
    signals, outputs = inputs
    digit_segments = {0: 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf',
                      5: 'abdfg', 6: 'abdefg', 7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
    segment_frequency_dict = {4: 'e', 6: 'b', 7: ('d', 'g'), 8: ('a', 'c'), 9: 'f'}
    output_sum = 0
    for signal, output in zip(signals, outputs):
        digit_dict = {}
        segment_dict = {}
        segment_frequency = Counter(''.join(signal))
        signal.sort(key=lambda x: len(x))

        # Gets the display for 1, 4, 7 and 8
        one_four_seven = []
        idx_dict = {1: 0, 4: 2, 7: 1, 8: 9}
        for i, v in idx_dict.items():
            digit_display = ''.join(sorted(signal[v]))
            if i in (1, 4, 7):
                one_four_seven.append(digit_display)
            digit_dict[digit_display] = i

        # Finds what 'a' would be by comparing 1 and 7
        a_segment = tuple((Counter(one_four_seven[2]) - Counter(one_four_seven[0])).keys())[0]
        segment_dict['a'] = a_segment

        # Finds 'd', 'b' and 'f' from frequencies, and 'c' from knowing it isn't 'a'
        # Also finds 'd' and 'g' as 'd' is in 4 and 'g' isn't
        for i, v in segment_frequency.items():
            if v in (4, 6, 9):
                segment_dict[segment_frequency_dict[v]] = i
            elif v == 8 and i != a_segment:
                segment_dict['c'] = i
            elif v == 7:
                segment_dict['d' if i in one_four_seven[1] else 'g'] = i

        # Fills out the digit dict
        for i in (0, 2, 3, 5, 6, 9):
            digit_as_list = [segment_dict[j] for j in digit_segments[i]]
            digit_dict[''.join(sorted(digit_as_list))] = i
        output_digit = ''
        for digit in output:
            output_digit += str(digit_dict[''.join(sorted(digit))])
        output_sum += int(output_digit)
    return output_sum


def display(output_sum) -> None:
    print(output_sum)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
