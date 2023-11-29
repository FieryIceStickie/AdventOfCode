import math
import re
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
        x1, x2, y1, y2 = [int(i) for i in re.match(r'target area: x=([-\d]+)\.\.([-\d]+), y=([-\d]+)\.\.([-\d]+)',
                          file.read().rstrip()).groups()]
        return sorted((x1, x2)) + sorted((y1, y2))


def floor_inverse_triangle(num: int) -> int:
    """
    The inverse of the triangular number function s.t f(nth triangular number) = n, with a floor function applied
    Turns negative -> positive
    """
    return math.floor(math.sqrt(abs(num)))


def triangle(num: int) -> int:
    """
    The triangular number function
    Turns negative -> positive
    """
    num = abs(num)
    return num * (num + 1) // 2


def y_sim(y: int, step: int) -> int:
    """
    Simulator for y
    :param y: starting velocity
    :param step: n
    :return: 1 if y-coord is positive, otherwise y-coord of a starting y velocity after n steps
    """
    if y > 0:
        step = step - 2 * y - 1
        if step < 0:
            return 1
        elif step == 0:
            return 0
        y = -y - 1
    return (step * (1 - step + 2 * y)) // 2


def y_gen(y_vel: int):
    y_pos = y_vel
    yield y_pos
    while True:
        y_vel -= 1
        y_pos += y_vel
        yield y_pos


def x_gen(x_vel: int):
    x_pos = x_vel
    yield x_pos
    sign = sgn(x_vel)
    new_x_vel = x_vel - sign
    while new_x_vel != 0:
        x_pos += new_x_vel
        yield x_pos
        new_x_vel -= sign
    while True:
        yield x_pos


def sgn(x: int) -> -1 | 0 | 1:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def solver(x_min: int, x_max: int, y_min: int, y_max: int) -> Any:
    velocity_count = (y_max - y_min + 1) * (x_max - x_min + 1)
    eligible_x: list = []
    for i in range(floor_inverse_triangle(x_min), x_min):
        x_sim = x_gen(i)
        x_count = 0
        step = 0
        lower_bound = 0
        is_stable = False
        while x_count <= x_max:
            x_prev = x_count
            x_count = next(x_sim)
            step += 1
            if x_min <= x_count and not lower_bound:
                lower_bound = step
            if x_prev == x_count:
                is_stable = True
                break
        if lower_bound and is_stable:
            eligible_x.append((i, lower_bound))
        elif lower_bound:
            eligible_x.append((i, (lower_bound, step)))
    y_upper = -y_min
    for i in eligible_x:
        match i:
            case x, (lower_bound, upper_bound):
                y_lower = y_min // lower_bound
                velocity_list = {(x, y) for y in range(y_lower, y_upper)
                                       for s in range(lower_bound, upper_bound) if y_min <= y_sim(y, s) <= y_max}
                velocity_count += len(velocity_list)
            case x, lower_bound:
                y_lower = y_min // lower_bound
                for y in range(y_lower, y_upper):
                    y_simm = y_gen(y)
                    y_count = 0
                    for _ in range(lower_bound):
                        y_count = next(y_simm)
                    while y_count >= y_min:
                        if y_max >= y_count:
                            velocity_count += 1
                            break
                        y_count = next(y_simm)
            case _:
                raise NotImplementedError
    return velocity_count


def display(count) -> None:
    print(count)


if __name__ == '__main__':
    answer = solver(*parser(
        file_name='day_17.txt',
        testing=False))
    display(answer)
