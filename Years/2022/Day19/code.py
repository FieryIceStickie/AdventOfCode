import re
from math import ceil


def parser(filename: str):
    with open(filename, 'r') as file:
        return [[*map(int, re.findall(r'\d+', line))] for line in file.read().splitlines()]


def part_a_solver(blueprints: list):
    quality = 0
    for bid, oo, co, obo, obc, go, gob in blueprints:
        max_ore = max(oo, co, obo, go)
        current_max = 0

        def dfs(ore, clay, obs, geode, orebot, claybot, obsbot, time):
            nonlocal current_max
            if time <= 0:
                current_max = max(current_max, geode)
                # print(ore, clay, obs, geode, orebot, claybot, obsbot, time)
                return
            elif geode + time * (time - 1) // 2 <= current_max:
                return
            # Build robots
            if max_ore > orebot:
                dt = max(ceil((oo - ore) / orebot), 0) + 1
                # print(dt)
                dfs(ore + orebot * dt - oo, clay + claybot * dt, obs + obsbot * dt, geode,
                    orebot + 1, claybot, obsbot,
                    time - dt)
            if obc > claybot:
                dt = max(ceil((co - ore) / orebot), 0) + 1
                # print(dt)
                dfs(ore + orebot * dt - co, clay + claybot * dt, obs + obsbot * dt, geode,
                    orebot, claybot + 1, obsbot,
                    time - dt)
            if gob > obsbot and claybot:
                dt = max(ceil((obo - ore) / orebot), ceil((obc - clay) / claybot), 0) + 1
                # print(dt)
                dfs(ore + orebot * dt - obo, clay + claybot * dt - obc, obs + obsbot * dt, geode,
                    orebot, claybot, obsbot + 1,
                    time - dt)
            if obsbot:
                dt = max(ceil((go - ore) / orebot), ceil((gob - obs) / obsbot), 0) + 1
                # print(dt)
                if dt < time:
                    dfs(ore + orebot * dt - go, clay + claybot * dt, obs + obsbot * dt - gob, geode + (time - dt),
                        orebot, claybot, obsbot,
                        time - dt)

        dfs(0, 0, 0, 0, 1, 0, 0, 24)
        quality += bid*current_max
        # print(bid, current_max)
    return quality


def part_b_solver(blueprints: list):
    geodes = 1
    for _, oo, co, obo, obc, go, gob in blueprints[:3]:
        max_ore = max(oo, co, obo, go)
        current_max = 0
        def dfs(ore, clay, obs, geode, orebot, claybot, obsbot, time):
            nonlocal current_max
            if time <= 0:
                current_max = max(current_max, geode)
                return
            elif geode + time*(time-1)//2 <= current_max:
                return
            # Build robots
            if max_ore > orebot:
                dt = max(ceil((oo-ore)/orebot), 0) + 1
                dfs(ore + orebot * dt - oo, clay + claybot * dt, obs + obsbot * dt, geode,
                    orebot + 1, claybot, obsbot,
                    time - dt)
            if obc > claybot:
                dt = max(ceil((co-ore)/orebot), 0) + 1
                dfs(ore + orebot * dt - co, clay + claybot * dt, obs + obsbot * dt, geode,
                    orebot, claybot + 1, obsbot,
                    time - dt)
            if gob > obsbot and claybot:
                dt = max(ceil((obo-ore)/orebot), ceil((obc-clay)/claybot), 0) + 1
                dfs(ore + orebot * dt - obo, clay + claybot * dt - obc, obs + obsbot * dt, geode,
                    orebot, claybot, obsbot + 1,
                    time - dt)
            if obsbot:
                dt = max(ceil((go-ore)/orebot), ceil((gob-obs)/obsbot), 0) + 1
                if dt < time:
                    dfs(ore + orebot * dt - go, clay + claybot * dt, obs + obsbot * dt - gob, geode + (time - dt),
                        orebot, claybot, obsbot,
                        time - dt)
        dfs(0, 0, 0, 0, 1, 0, 0, 32)
        geodes *= current_max
    return geodes


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
