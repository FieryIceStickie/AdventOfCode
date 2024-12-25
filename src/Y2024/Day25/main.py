from typing import TextIO


def parser(raw_data: TextIO):
    keys = set()
    locks = set()
    for grid in raw_data.read().split('\n\n'):
        lines = grid.splitlines()
        if lines[0] == '#####':
            s = keys
            lines = lines[1:]
        else:
            s = locks
            lines = lines[:-1]
        s.add(tuple(sum(v == '#' for v in row) for row in zip(*lines)))
    return keys, locks


def solver(keys, locks):
    return sum(
        all(a + b <= 5 for a, b in zip(key, lock))
        for key in keys
        for lock in locks
    )


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

    print(solver(*data))
