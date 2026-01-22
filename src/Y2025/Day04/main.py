from typing import TextIO


def parser(raw_data: TextIO) -> set[complex]:
    return {
        x + 1j * y
        for x, row in enumerate(raw_data.read().splitlines())
        for y, v in enumerate(row)
        if v == '@'
    }

deltas = (-1-1j, -1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1)

def full_solver(grid: set[complex]) -> tuple[int, int]:
    scores: dict[complex, int] = {}
    bfs: list[complex] = []
    for z in grid:
        scores[z] = sum(z + dz in grid for dz in deltas)
        if scores[z] < 4:
            bfs.append(z)

    p1 = len(bfs)
    for z in bfs:
        for dz in deltas:
            p = z + dz
            if p not in grid:
                continue
            scores[p] -= 1
            if scores[p] == 3:
                bfs.append(p)

    return p1, len(bfs)


if __name__ == '__main__':
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = 'evil.txt'
    else:
        path = test_path if testing else 'input.txt'

    with open(path, 'r') as file:
        data = parser(file)

    print(*full_solver(data))
