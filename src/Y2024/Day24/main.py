from typing import TextIO, Self, ClassVar
import re
from operator import and_, or_, xor

from attrs import define
from functools import total_ordering


def parser(raw_data: TextIO):
    value_str, eqn_str = raw_data.read().split('\n\n')
    values = {
        k: int(v) for k, v in re.findall(r'(\w+): (\d)', value_str)
    }
    eqns = {
        res: (op, a, b)
        for a, op, b, res in re.findall(r'(\w+) (\w+) (\w+) -> (\w+)', eqn_str)
    }
    z_count = len(values) // 2 + 1
    return values, eqns, z_count


@total_ordering
@define(frozen=True, order=False, match_args=True)
class Node:
    prio_dict: ClassVar[dict[str, int]] = {'XOR': 0, 'AND': 1, 'OR': 2}
    name: str
    op: str
    left: str | Self
    right: str | Self
    value: int

    def __lt__(self, other):
        if isinstance(other, str):
            return True
        if self.op != other.op:
            return self.prio_dict[self.op] < self.prio_dict[other.op]
        if isinstance(self.left, str) and isinstance(other.left, str):
            return self.left[0] in 'xy'
        return self.left < other.left


def name(s: str | Node) -> str:
    match s:
        case str(): return s
        case Node(name=s): return s


def full_solver(values: dict[str, int], eqns: dict[str, tuple[str, str, str]], z_count: int):
    swaps = set()
    op_dict = {'AND': and_, 'OR': or_, 'XOR': xor}

    def traverse(node: str) -> str | Node:
        nonlocal jumper
        if node in jumper or node not in eqns:
            return node
        op, a, b = eqns[node]
        a, b = traverse(a), traverse(b)
        if b < a: a, b = b, a
        res = op_dict[op](values[name(a)], values[name(b)])
        values[node] = res
        return Node(node, op, a, b, res)

    jumper = set()
    for z in range(z_count):
        tree = traverse(f'z{z:02}')
        if res := matcher(tree, z, jumper):
            swaps.add(res)
        try:
            jumper = {tree.left.name, tree.right.name}
        except AttributeError:
            jumper = set()
    return (
        int(''.join(str(values[f'z{z:02}']) for z in range(z_count))[::-1], 2),
        ','.join(sorted(swaps))
    )


def matcher(tree: Node, z: int, jumper: set[str]):
    if z < 3 or z == 45:
        return
    match tree:
        case Node(name=name, op=op) if op != 'XOR':
            return name
        case Node(
            left=Node(name=name, op=op, left=left, right=right)
        ) if op != 'XOR' or {left, right} != {f'x{z:02}', f'y{z:02}'}:
            return name
        case Node(
            op='XOR',
            right=Node(name=name, op=op),
        ) if op != 'OR':
            return name
        case Node(
            op='XOR',
            right=Node(
                op='OR',
                left=Node(name=name, op=op, left=left, right=right),
            )
        ) if op != 'AND' or {left, right} != {f'x{z - 1:02}', f'y{z - 1:02}'}:
            return name
        case Node(
            op='XOR',
            right=Node(
                op='OR',
                right=Node(name=name, op=op, left=left, right=right),
            )
        ) if op != 'AND' or {left, right} != jumper:
            return name


if __name__ == '__main__':
    testing = False

    try:
        from Tools.Python.path_stuff import test_path
    except ModuleNotFoundError:
        path = 'input.txt'
    else:
        path = test_path if testing else 'input.txt'

    with open(path, 'r') as file:
        data = parser(file)

    print(*full_solver(*data))
