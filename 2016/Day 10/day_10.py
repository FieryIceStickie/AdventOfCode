from typing import TextIO
import re
from collections import defaultdict, deque
from math import prod
from operator import itemgetter

from path_stuff import *


def parser(raw_data: TextIO):
    bots, instructions = defaultdict(list), {}
    setup_pattern = re.compile(r'value (\d+) goes to bot (\d+)')
    give_pattern = re.compile(r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)')
    for line in raw_data.read().splitlines():
        if match := setup_pattern.match(line):
            value, bot = map(int, match.groups())
            bots[bot].append(value)
        elif match := give_pattern.match(line) :
            bot, lt, lb, ht, hb = match.groups()
            bot, lb, hb = map(int, (bot, lb, hb))
            instructions[bot] = (lt == 'output', lb, ht == 'output', hb)
    return bots, instructions


def simulate(bots: defaultdict[int, list[int]], instructions: dict[int, tuple[bool, int, bool, int]]):
    outputs = defaultdict(list)
    active = deque([next(bot for bot, values in bots.items() if len(values) > 1)])
    part_1 = None
    while active:
        bot = active.popleft()
        lv, hv = sorted(bots[bot])
        if (lv, hv) == (17, 61):
            part_1 = bot
        lt, lb, ht, hb = instructions[bot]
        if not lt and bots[lb]:
            active.append(lb)
        [bots, outputs][lt][lb].append(lv)
        if not ht and bots[hb]:
            active.append(hb)
        [bots, outputs][ht][hb].append(hv)
    return part_1, prod(map(itemgetter(0), itemgetter(0, 1, 2)(outputs)))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else root_path / '2016/Day 10/day_10.txt', 'r') as file:
        bots, instructions = parser(file)
    print(simulate(bots, instructions))
