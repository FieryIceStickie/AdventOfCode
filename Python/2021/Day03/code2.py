from functools import reduce
from typing import Any

from Python.path_stuff import *


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return file.read().splitlines()
    if len(inputs) == 0 and testing:
        with open(test_path, 'r') as file:
            return file.read().splitlines()
    return inputs


def to_dec(bin_num: str) -> int:
    bin_num = reversed(list(bin_num))
    dec_num = 0
    for p, v in enumerate(bin_num):
        dec_num += int(v) * 2 ** p
    return dec_num


def most_common_bits(arr: list) -> list:
    mid_length = len(arr) / 2
    one_frequencies = reduce(lambda x, y: tuple(sum([int(iii) for iii in ii]) for ii in zip(x, y)), arr)
    common_bits = []
    for i in one_frequencies:
        if i >= mid_length:
            common_bits.append('1')
        elif i < mid_length:
            common_bits.append('0')
    return common_bits


def solver(inputs: Any) -> Any:
    o2_candidates = inputs
    o2_i = 0
    while len(o2_candidates) > 1:
        o2_common_bits = most_common_bits(o2_candidates)
        o2_candidates = list(filter(lambda x: x[o2_i] == o2_common_bits[o2_i], o2_candidates))
        o2_i += 1
    o2 = list(o2_candidates)[0]
    co2_candidates = inputs
    co2_i = 0
    while len(co2_candidates) > 1:
        co2_common_bits = ['0' if i == '1' else '1' for i in most_common_bits(co2_candidates)]
        co2_candidates = list(filter(lambda x: x[co2_i] == co2_common_bits[co2_i], co2_candidates))
        co2_i += 1
    co2 = list(co2_candidates)[0]
    print(to_dec(o2), to_dec(co2))
    return to_dec(o2) * to_dec(co2)


def display(product) -> None:
    print(product)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='input.txt',
        testing=False))
    display(answer)
