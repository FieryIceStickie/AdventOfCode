def parser(filename: str):
    with open(filename, 'r') as file:
        return [[*map(int,elf.splitlines())] for elf in file.read().split('\n\n')]


def part_a_solver(calorie_list: list):
    return max(map(sum, calorie_list))


def part_b_solver(calorie_list: list):
    return sum(sorted(map(sum, calorie_list), reverse=True)[:3])


if __name__ == '__main__':
    inputs = parser('day_1.txt')
    print(part_a_solver(inputs.copy()))
    print(part_b_solver(inputs))
