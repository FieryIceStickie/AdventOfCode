from typing import Any
import numpy as np


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if not testing:
        with open(file_name, 'r') as file:
            return np.array(file.read().split(','), dtype=int)
    if len(inputs) == 0 and testing:
        with open('test.txt', 'r') as file:
            return np.array(file.read().split(','), dtype=int)
    return inputs


def fish_sim(added_fish_per_day: np.ndarray):
    day_of_week = 0
    population = np.sum(added_fish_per_day)
    baby_fish = np.zeros(7, dtype=int)
    while True:
        population += added_fish_per_day[day_of_week]
        baby_fish[(day_of_week + 2) % 7] = added_fish_per_day[day_of_week]
        added_fish_per_day[day_of_week] += baby_fish[day_of_week]
        baby_fish[day_of_week] = 0
        day_of_week = (day_of_week + 1) % 7
        yield population


def solver(inputs: Any) -> Any:
    added_fish_per_day = np.zeros(7, dtype=int)
    for i in inputs:
        added_fish_per_day[i] += 1
    sim = fish_sim(added_fish_per_day)
    population = 0
    for i in range(256):
        population = next(sim)
    return population


def display(population) -> None:
    print(population)


if __name__ == '__main__':
    answer = solver(parser(

        file_name='day_6.txt',
        testing=False))
    display(answer)
