from collections import deque
from itertools import count, repeat
from math import lcm
from typing import TextIO

from Tools.Python.path_stuff import *


def parser(raw_data: TextIO):
    memory = {}
    broadcaster = None
    for line in raw_data.read().splitlines():
        name, outputs = line.split(' -> ')
        outputs = outputs.split(', ')
        if name == 'broadcaster':
            broadcaster = outputs
        elif name.startswith('%'):
            memory[name[1:]] = [False, outputs]
        elif name.startswith('&'):
            memory[name[1:]] = [{}, outputs]
        else:
            raise ValueError('weird input')
    for name, (_, outputs) in memory.items():
        for output in outputs:
            if isinstance(gate_data := memory.get(output, [1])[0], dict):
                gate_data[name] = False
    return broadcaster, memory


def part_a_solver(broadcaster: list[str], memory: dict[str, list[bool | dict[str, bool], list[str]]]):
    low, high = 0, 0
    def sim():
        nonlocal low, high
        low += 1
        active = deque(zip(repeat('broadcaster'), repeat(False), broadcaster))
        while active:
            prev, signal, node = active.popleft()
            if signal:
                high += 1
            else:
                low += 1
            gate = memory.get(node)
            if gate is None:
                continue
            gate_data, outputs = gate
            if isinstance(gate_data, bool):
                if not signal:
                    gate[0] = not gate_data
                    active.extend((node, gate[0], output) for output in outputs)
            else:
                gate_data[prev] = signal
                new_signal = not all(gate_data.values())
                active.extend((node, new_signal, output) for output in outputs)
    for i in range(1000):
        sim()
    return low * high


def part_b_solver(broadcaster: list[str], memory: dict[str, list[bool | dict[str, bool], list[str]]]):
    def sim(start: str):
        active = deque([['broadcaster', 0, start]])
        while active:
            prev, signal, node = active.popleft()
            if node == 'sq' and signal:
                return True
            gate = memory.get(node)
            if gate is None:
                continue
            gate_data, outputs = gate
            if isinstance(gate_data, bool):
                if not signal:
                    gate[0] = not gate_data
                    active.extend((node, gate[0], output) for output in outputs)
            else:
                gate_data[prev] = signal
                new_signal = not all(gate_data.values())
                active.extend((node, new_signal, output) for output in outputs)
        return False
    return lcm(*[next(i for i in count(1) if sim(node)) for node in broadcaster])


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        main_broadcaster, main_memory = parser(file)

    copied_memory = {
        name: [gate_data, [*outputs]] if isinstance(gate_data, bool) else [{**gate_data}, [*outputs]]
        for name, (gate_data, outputs) in main_memory.items()
    }
    print(part_a_solver(main_broadcaster, main_memory))
    print(part_b_solver(main_broadcaster, copied_memory))
