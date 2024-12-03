from typing import Any

import numpy as np

from Tools.Python.path_stuff import *


def parser(testing_input: Any, file_name: str = '', is_testing: bool = False) -> Any:
    if is_testing:
        if testing_input is None:
            file_to_read = test_path
        else:
            return testing_input
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        east_cucumbers, south_cucumbers = set(), set()
        read_file = np.array([list(i) for i in file.read().splitlines()])
        x_len, y_len = np.shape(read_file)
        for x, line in enumerate(read_file):
            for y, v in enumerate(line):
                match v:
                    case '>':
                        east_cucumbers.add(complex(x, y))
                    case 'v':
                        south_cucumbers.add(complex(x, y))
                    case _:
                        pass
        return east_cucumbers, south_cucumbers, x_len, y_len


def solver(easts: set, souths: set, x_len: int, y_len: int) -> Any:

    def display_area(current_easts: set, current_souths: set):
        arr = np.zeros((x_len, y_len))
        for cucumber_loc in current_easts:
            arr[(int(cucumber_loc.real), int(cucumber_loc.imag))] = 1
        for cucumber_loc in current_souths:
            arr[(int(cucumber_loc.real), int(cucumber_loc.imag))] = 2
        display_dict = {0: '.', 1: '>', 2: 'v'}
        for line in arr:
            for v in line:
                print(display_dict[v], end='')
            print('')
        print('\n')

    def get_forward(cucumber_loc: complex, cucumber_type: bool) -> complex:
        if not cucumber_type:
            return complex(cucumber_loc.real, (cucumber_loc.imag + 1) % y_len)
        else:
            return complex((cucumber_loc.real + 1) % x_len, cucumber_loc.imag)

    steps = 0
    is_display = False
    while True:
        has_moved = False
        steps += 1
        moves = set()
        for loc in easts:
            forward = get_forward(loc, False)
            if forward not in easts and forward not in souths:
                moves.add((loc, forward))
        if moves:
            has_moved = True
        for loc, forward in moves:
            easts.add(forward)
            easts.remove(loc)

        moves = set()
        for loc in souths:
            forward = get_forward(loc, True)
            if forward not in easts and forward not in souths:
                moves.add((loc, forward))
        if moves:
            has_moved = True
        for loc, forward in moves:
            souths.add(forward)
            souths.remove(loc)

        if is_display:
            display_area(easts, souths)
        if not has_moved:
            break
    return steps


def display(steps) -> None:
    print(steps)


if __name__ == '__main__':
    profiling = False
    test_input = None
    testing = False
    if profiling:
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            answer = solver(*parser(test_input,
                                    file_name='input.txt',
                                    is_testing=testing))
            display(answer)

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename='profiling.prof')
    else:
        answer = solver(*parser(test_input,
                                file_name='input.txt',
                                is_testing=testing))
        display(answer)
