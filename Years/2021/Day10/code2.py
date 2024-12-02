from typing import Any

from Years.path_stuff import *


class CorruptedLineError(Exception):
    pass


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return [list(i) for i in file.read().splitlines()]
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            return [list(i) for i in file.read().splitlines()]
    return inputs


def solver(inputs: Any) -> Any:
    close_bracket_dict = {')': '(', ']': '[', '}': '{', '>': '<'}
    bracket_score_dict = {'(': 1, '[': 2, '{': 3, '<': 4}
    scores = []
    for lines in inputs:
        stack = []
        try:
            for i in lines:
                if i in ('(', '[', '{', '<'):
                    stack.append(i)
                elif i in (')', ']', '}', '>'):
                    if stack[-1] == close_bracket_dict.get(i):
                        stack = stack[:-1]
                    else:
                        raise CorruptedLineError(i)
                else:
                    raise NotImplementedError
        except CorruptedLineError:
            pass
        else:
            score = 0
            for i in stack[::-1]:
                score *= 5
                score += bracket_score_dict.get(i)
            scores.append(score)
    scores.sort()
    middle = scores[(len(scores) - 1) // 2]
    return middle


def display(middle) -> None:
    print(middle)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
