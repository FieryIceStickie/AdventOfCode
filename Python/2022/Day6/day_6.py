from more_itertools import windowed


def parser(filename: str):
    with open(filename, 'r') as file:
        return file.read()


def part_a_solver(data: str):
    return next(i + 4 for i, v in enumerate(windowed(data, 4)) if len(set(v)) == 4)


def part_b_solver(data: str):
    return next(i + 14 for i, v in enumerate(windowed(data, 14)) if len(set(v)) == 14)


if __name__ == '__main__':
    inputs = parser('day_6.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
