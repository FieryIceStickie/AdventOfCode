def parser(filename: str):
    with open(filename, 'r') as file:
        return [i.split() for i in file.read().splitlines()]


def part_a_solver(moves: list[list[str, str]]):
    return sum(smove + [3, 6, 0][(smove - emove) % 3]
               for emove, smove in ((' ABC'.index(i), ' XYZ'.index(j)) for i, j in moves))


def part_b_solver(moves: list[list[str, str]]):
    move_dict = {'A': 1, 'B': 2, 'C': 3, 0: 3, 1: 1, 2: 2}
    offset_dict = {'X': 2, 'Y': 0, 'Z': 1}
    score_dict = {'X': 0, 'Y': 3, 'Z': 6}
    return sum([3,1,2][(' ABC'.index(move) + 'YZX'.index(result)) % 3] + 'X  Y  Z'.index(result)
               for move, result in moves)


if __name__ == '__main__':
    inputs = parser('day_2.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
