from typing import TextIO, Iterator
from bitarray import bitarray

from path_stuff import *


def parser(raw_data: TextIO):
    return bitarray(raw_data.read())


def gen_curve(data: bitarray) -> Iterator[bitarray]:
    while True:
        data = data + [0] + ~data[::-1]
        yield data


def checksum(data: bitarray) -> str:
    while not len(data) & 1:
        data = [i == j for i, j in zip(*[iter(data)]*2)]
    return ''.join(map(str, map(int, data)))


def part_a_solver(data: bitarray):
    return checksum(next(i for i in gen_curve(data) if len(i) >= 272)[:272])


def part_b_solver(data: bitarray):
    return checksum(next(i for i in gen_curve(data) if len(i) >= 35651584)[:35651584])


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 16/day_16.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
