from typing import Any

from Tools.Python.path_stuff import *


class CorruptedLineError(Exception):
    def __init__(self, bracket: str):
        self.bracket = bracket


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
    bracket_score_dict = {')': 3, ']': 57, '}': 1197, '>': 25137}
    score = 0
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
        except CorruptedLineError as e:
            score += bracket_score_dict.get(e.bracket)
    return score


def display(score) -> None:
    print(score)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
