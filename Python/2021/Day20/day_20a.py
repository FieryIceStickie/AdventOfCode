import cProfile
import pstats
from typing import Any


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = 'test.txt'
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        lines = file.read().splitlines()
        algorithm = {i: v == '#' for i, v in enumerate(lines[0])}
        points = [complex(r, i) for i, ii in enumerate(lines[2:]) for r, v in enumerate(ii) if v == '#']
        return algorithm, set(points)


def solver(algorithm: dict, points: set[complex, ...]) -> int:
    points = image_double_enhance(algorithm, points)
    return len(points)


def image_double_enhance(algorithm: dict, points: set[complex, ...]) -> set[complex, ...]:
    if algorithm[0]:
        first_point_candidates = set(i for pt in points for i in square_pixels(pt))
        first_not_points = set(pt for pt in first_point_candidates
                               if not algorithm[bin2dec(*[i in points for i in square_pixels(pt)])])
        second_point_candidates = set(i for pt in first_not_points for i in square_pixels(pt))
        return set(pt for pt in second_point_candidates
                   if algorithm[bin2dec(*[i not in first_not_points for i in square_pixels(pt)])])
    else:
        first_point_candidates = set(i for pt in points for i in square_pixels(pt))
        first_points = set(pt for pt in first_point_candidates
                           if algorithm[bin2dec(*[i in points for i in square_pixels(pt)])])
        second_point_candidates = set(i for pt in first_points for i in square_pixels(pt))
        return set(pt for pt in second_point_candidates
                           if algorithm[bin2dec(*[i in first_points for i in square_pixels(pt)])])


def bin2dec(*digits: bool):
    num = ''.join(['1' if i else '0' for i in digits])
    return int(f'0b{num}', 2)


def square_pixels(point: complex) -> list[complex]:
    """
    Returns surrounding points of a point
    :param point: The point
    :return: A list of surrounding points
    """
    return [point + delta for delta in (-1-1j, -1j, 1-1j, -1, 0, 1, -1+1j, 1j, 1+1j)]


def display(lit_count) -> None:
    print(lit_count)


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        answer = solver(*parser(
            file_name='day_20.txt',
            testing=False))
        display(answer)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')
