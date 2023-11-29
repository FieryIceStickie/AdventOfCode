from string import ascii_lowercase, ascii_uppercase
from more_itertools import chunked


def parser(filename: str):
    with open(filename, 'r') as file:
        return file.read().splitlines()


priority_dict = {**{i: ord(i) - 96 for i in 'abcdefghijklmnopqrstuvwxyz'},
                 **{i: ord(i) - 38 for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}}


def part_a_solver(rucksacks: list[str]):
    return sum(priority_dict[({*i[:(halfway := len(i) // 2)]}&{*i[halfway:]}).pop()] for i in rucksacks)


def part_b_solver(rucksacks: list[str]):
    return sum(priority_dict[({*x}&{*y}&{*z}).pop()] for x, y, z in chunked(rucksacks, 3))


if __name__ == '__main__':
    inputs = parser('day_3.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
