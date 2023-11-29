import re
from functools import cache
from operator import add, mul, sub, truediv

from attrs import Factory, define


def parser(filename: str):
    with open(filename, 'r') as file:
        return {k: int(v[0]) if len(v)==1 else v for k, *v in [re.match(r'(\w{4}): (\d+)', i).groups()
                if i[-1].isdigit()
                else re.match(r'(\w{4}): (\w{4}) ([-+*/]) (\w{4})', i).groups()
                for i in file.read().splitlines()]}


def part_a_solver(monkeys: dict[str, list[str, str, str]|int]):
    @cache
    def yell(monkey):
        match monkeys[monkey]:
            case fir, op, sec:
                return {'+': add, '-': sub, '*': mul, '/': truediv}[op](yell(fir), yell(sec))
            case num:
                return num
    return int(yell('root'))

@define
class Human:
    operations: list = Factory(list)
    def __add__(self, other):
        self.operations.append(('+', other))
        return self
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        self.operations.append(('-', other))
        return self
    def __rsub__(self, other):
        self.operations.append((other, '-'))
        return self
    def __mul__(self, other):
        self.operations.append(('*', other))
        return self
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        self.operations.append(('/', other))
        return self
    def __rtruediv__(self, other):
        self.operations.append((other, '/'))
        return self

def part_b_solver(monkeys: dict[str, list[str, str, str]|int|Human]):
    monkeys['humn'] = Human()
    @cache
    def yell(monkey):
        match monkeys[monkey]:
            case fir, op, sec:
                return {'+': add, '-': sub, '*': mul, '/': truediv}[op](yell(fir), yell(sec))
            case num:
                return num
    left, _, right = monkeys['root']
    # Hard coded left as human right as number
    answer = yell(right)
    for instruction in reversed(yell(left).operations):
        match instruction:
            case '+', num:
                answer -= num
            case '-', num:
                answer += num
            case '*', num:
                answer /= num
            case '/', num:
                answer *= num
            case num, '-':
                answer = num - answer
            case num, '/':
                answer = num / answer
    return int(answer)

if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
