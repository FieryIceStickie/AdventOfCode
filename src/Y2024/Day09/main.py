from typing import TextIO, Protocol, Self
from itertools import chain, takewhile

from attrs import frozen

from Tools.Python.path_stuff import *
from Tools.Python.utils import reversed_enumerate, sum_range


class Block(Protocol):
    @property
    def size(self) -> int:
        pass

    @property
    def space(self) -> int:
        pass

    def can_move(self) -> bool:
        pass

    def value(self, idx: int) -> int:
        pass

    def set_block(self, block: Self) -> Self:
        pass

    def clear(self) -> Self:
        pass


@frozen
class SingleBlock(Block):
    _size: int
    id: int | None

    @property
    def size(self) -> int:
        return self._size

    @property
    def space(self) -> int:
        return self.size if self.id is None else 0

    def can_move(self) -> bool:
        return self.id is not None

    def value(self, idx: int) -> int:
        if self.id is None:
            return 0
        return self.id * sum_range(idx, idx + self.size)

    def set_block(self, block: Block) -> Block:
        return MultiBlock(block, SingleBlock(self.size - block.size, None))

    def clear(self) -> Block:
        return SingleBlock(self.size, None)

    def __str__(self):
        return f'{self.id if self.id is not None else '.'}' * self.size


@frozen
class MultiBlock(Block):
    left: Block
    right: Block

    @property
    def size(self) -> int:
        return self.left.size + self.right.size

    @property
    def space(self) -> int:
        return self.right.space

    def can_move(self) -> bool:
        return False

    def value(self, idx: int) -> int:
        return self.left.value(idx) + self.right.value(idx + self.left.size)

    def set_block(self, block: Block) -> Block:
        return MultiBlock(self.left, self.right.set_block(block))

    def clear(self) -> Block:
        raise NotImplementedError

    def __str__(self):
        return f'{self.left}{self.right}'


def parser(raw_data: TextIO):
    return [
        SingleBlock(int(size), idx // 2 if not idx % 2 else None)
        for idx, size in enumerate(raw_data.read())
    ]


def part_a_solver(data: list[SingleBlock]):
    *data, = chain(
        idx // 2 if not idx % 2 else None
        for idx, block in enumerate(data)
        for _ in range(block.size)
    )
    start = 0
    end = len(data) - 1
    while True:
        while data[start] is not None:
            start += 1
        while data[end] is None:
            end -= 1
        if start >= end:
            break
        data[start], data[end] = data[end], data[start]
    return sum(
        i * v
        for i, v in enumerate(
            takewhile(lambda x: x is not None, data)
        )
    )


def part_b_solver(data: list[Block]):
    for block_idx, block in reversed_enumerate(data):
        if not block.can_move():
            continue
        for slot_idx, slot in enumerate(data[:block_idx]):
            if not slot.can_move() and slot.space >= block.size:
                data[slot_idx] = data[slot_idx].set_block(block)
                data[block_idx] = data[block_idx].clear()
                break
    s = 0
    idx = 0
    for block in data:
        s += block.value(idx)
        idx += block.size
    return s


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(part_a_solver(data))
    print(part_b_solver(data))
