from typing import Any
import numpy as np


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return np.array(tuple(tuple(i) for i in file.read().splitlines()), dtype=int)
    if len(inputs) == 0 and testing:
        with open('test.txt', 'r') as file:
            return np.array(tuple(tuple(i) for i in file.read().splitlines()), dtype=int)
    return inputs


class Grid:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.flashes = 0

    def step(self):
        new_grid = self.grid + 1
        flashing_pts = [(xn, yn) for xn, yn in np.column_stack(np.nonzero(new_grid > 9))]
        flashed_neighbours = []
        # sum(arr, []) flattens the list
        for pt in flashing_pts:
            flashed_neighbours.append(get_surrounding_points(*pt))
        flashed_neighbours = sum(flashed_neighbours, [])
        while flashed_neighbours:
            for pt in flashed_neighbours:
                new_grid[pt] += 1
            new_flashes = [(xn, yn) for xn, yn in np.column_stack(np.nonzero(new_grid > 9))
                           if (xn, yn) not in flashing_pts]
            flashed_neighbours = sum([get_surrounding_points(*ptn) for ptn in new_flashes], [])
            flashing_pts += new_flashes
        self.flashes += len(flashing_pts)
        for pt in flashing_pts:
            new_grid[pt] = 0
        self.grid = new_grid

    def __str__(self):
        rtn_str = ''
        for i in self.grid:
            for j in i:
                rtn_str += str(j)
            rtn_str += '\n'
        return rtn_str


def get_surrounding_points(xn: int, yn: int) -> list[tuple[int, int]]:
    pts = [(xn - 1, yn), (xn - 1, yn + 1), (xn, yn + 1), (xn + 1, yn + 1),
           (xn + 1, yn), (xn + 1, yn - 1), (xn, yn - 1), (xn - 1, yn - 1)]
    pts = [(x, y) for x, y in pts if 10 > x >= 0 and 10 > y >= 0]
    return pts


def solver(inputs: Any) -> Any:
    grid = Grid(inputs)
    i = 0
    while True:
        i += 1
        grid.step()
        if not np.any(grid.grid):
            break
    return i


def display(iterations) -> None:
    print(iterations)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='day_11.txt',
        testing=False))
    display(answer)
