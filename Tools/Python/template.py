from typing import TextIO


def parser(raw_data: TextIO):
    return raw_data.read().splitlines()


def part_a_solver(data):
    return


def part_b_solver(data):
    return


if __name__ == '__main__':
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = 'input.txt'
    else:
        path = test_path if testing else 'input.txt'

    with open(path, 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
