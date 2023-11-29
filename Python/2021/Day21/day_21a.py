import cProfile
import pstats
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
        rtn = []
        for line in file.read().splitlines():
            rtn.append(int(re.match(r'Player \d starting position: (\d{1,2})', line).groups()[0]))
        return rtn


def solver(player_one_pos: int, player_two_pos: int) -> Any:
    die = 2
    roll_count = 0
    scores = [0, 0]
    player = False
    pos = [player_one_pos, player_two_pos]
    while max(scores) < 1000:
        match die:
            case 100:
                roll = 200
            case 1:
                roll = 103
            case _:
                roll = 3 * die
        die = (die + 2) % 100 + 1
        pos[player] = (pos[player] + roll - 1) % 10 + 1
        scores[player] += pos[player]
        roll_count += 3
        player = not player
    return min(scores) * roll_count


def display(score) -> None:
    print(score)


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        answer = solver(*parser(
            file_name='day_21.txt',
            testing=False))
        display(answer)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')
