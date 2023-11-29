import math as m


def parser(filename: str):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def part_a_solver(numbers: list[str]):
    str_to_int = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
    int_to_str = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    num_sum = sum(sum(str_to_int[v] * 5 ** i for i, v in enumerate(n[::-1])) for n in numbers)
    quin_rep = [num_sum // (5 ** b) % 5 for b in range(m.floor(m.log(num_sum, 5)) + 1)]
    for i, j in enumerate(quin_rep[:-1]):
        quin_rep[i + 1] += (j in (3, 4, 5))
        quin_rep[i] = {3: -2, 4: -1, 5: 0}.get(j, j)
    return ''.join(int_to_str[v] for v in quin_rep[::-1])


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs))
