def parser(filename: str):
    with open(filename, 'r') as file:
        return [[tuple(map(int, j.split('-')))
                 for j in i.split(',')]
                for i in file.read().splitlines()]


def part_a_solver(pairs: list[list[tuple[int, ...]]]):
    return len([1 for (a, b), (x, y) in pairs if (a <= x and b >= y) or (a >= x and b <= y)])


def part_b_solver(pairs: list[list[tuple[int, ...]]]):
    return len([1 for (a, b), (x, y) in pairs if max(a, x) <= min(b, y)])


if __name__ == '__main__':
    inputs = parser('day_4.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
