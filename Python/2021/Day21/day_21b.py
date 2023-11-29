from typing import Any
import cProfile
import pstats
import re
from typing import NamedTuple
from collections import Counter
from itertools import product
from functools import cache


# noinspection PyTypeChecker
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
        return Game(0j, tuple(rtn), False)


class Game(NamedTuple):
    scores: complex
    pos: tuple[int, int]
    player: bool

    def play(self, roll: 1 | 2 | 3):
        if not self.player:
            new_pos = ((self.pos[0] + roll - 1) % 10 + 1, self.pos[1])
            new_scores = self.scores + new_pos[0]
        else:
            new_pos = (self.pos[0], (self.pos[1] + roll - 1) % 10 + 1)
            new_scores = self.scores + new_pos[1] * 1j
        return Game(new_scores, new_pos, not self.player)


def solver(game) -> Any:
    # Main idea of this was from salt from the python discord
    roll_frequencies = Counter(sum(i) for i in product((1, 2, 3), repeat=3))

    @cache
    def find_scores(game_object) -> complex:
        if game_object.scores.real >= 21:
            return 1
        elif game_object.scores.imag >= 21:
            return 1j
        return sum(v * find_scores(game_object.play(i)) for i, v in roll_frequencies.items())

    scores = find_scores(game).real
    return int(max(scores.real, scores.imag))


def display(universes) -> None:
    print(universes)


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        answer = solver(parser(
            file_name='day_21.txt',
            testing=False))
        display(answer)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')
