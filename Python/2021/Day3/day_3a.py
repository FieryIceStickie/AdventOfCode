from typing import Any
from functools import reduce


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return file.read().splitlines()
    if len(inputs) == 0 and testing:
        with open('test.txt', 'r') as file:
            return file.read().splitlines()
    return inputs


def to_dec(bin_num: list[str]) -> int:
    bin_num.reverse()
    dec_num = 0
    for p, v in enumerate(bin_num):
        dec_num += int(v)*2**p
    return dec_num


def solver(inputs: Any) -> Any:
    mid_length = len(inputs) / 2
    one_frequencies = reduce(lambda x, y: tuple(sum([int(iii) for iii in ii]) for ii in zip(x, y)), inputs)
    gamma = []
    for i in one_frequencies:
        if i == mid_length:
            raise NotImplemented
        elif i > mid_length:
            gamma.append('1')
        elif i < mid_length:
            gamma.append('0')
    epsilon = ['0' if i == '1' else '1' for i in gamma]
    return to_dec(gamma) * to_dec(epsilon)


def display(product) -> None:
    print(product)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='day_3.txt',
        testing=False))
    display(answer)
