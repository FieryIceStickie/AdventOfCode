from collections.abc import Callable, Iterable, Iterator
from typing import TextIO
import re
from operator import and_, or_, xor
import ast

type Op = Callable[[int, int], int]
type Eqn = tuple[str, str, str]


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


def full_solver(values: dict[str, int], eqns: dict[str, Eqn], z_count: int):
    pass


def calculate(
        targets: Iterable[str],
        values: dict[str, int],
        eqns: dict[str, tuple[Op, str, str]]
) -> Iterator[int]:
    def calc(target):
        if target in values:
            return values[target]
        op, a, b = eqns[target]
        res = op(calc(a), calc(b))
        values[target] = res
        return res

    return map(calc, targets)


def part_a_solver(values: dict[str, int], eqns: dict[str, Eqn]):
    targets = sorted(
        name for name in eqns
        if name.startswith('z')
    )
    values = values.copy()
    op_dict = {'AND': and_, 'OR': or_, 'XOR': xor}
    eqns = {res: (op_dict[op], a, b) for res, (op, a, b) in eqns.items()}
    res = calculate(targets, values, eqns)
    return int(''.join(map(str, res))[::-1], 2)


# def part_b_solver(values: dict[str, int], eqns: dict[str, Eqn]):
#     pass


def part_b_solver(values: dict[str, int], eqns: dict[str, Eqn]):
    names = {*values}
    op_dict = {'AND': ast.BitAnd(), 'OR': ast.BitOr(), 'XOR': ast.BitXor()}
    targets = sorted(
        name for name in eqns
        if name.startswith('z')
    )
    eqns = {
        res: ast.BinOp(
            left=ast.Name(a),
            op=op_dict[op],
            right=ast.Name(b)
        )
        for res, (op, a, b) in eqns.items()
    }

    def swap(k1, k2):
        eqns[k1], eqns[k2] = eqns[k2], eqns[k1]
    swap('z06', 'dhg')
    swap('brk', 'dpd')
    swap('z23', 'bhd')
    swap('z38', 'nbf')
    [*trees], vals = make_trees(targets, names, eqns)

    for tree in trees:
        print(ast.unparse(tree))
    print()
    for name, (eqn, *_) in vals.items():
        print(name, ast.unparse(eqn))
    print(','.join(sorted(['z38', 'nbf', 'z23', 'bhd', 'brk', 'dpd', 'z06', 'dhg'])))
    return


def make_trees(
    targets: Iterable[str],
    names: set[str],
    eqns: dict[str, ast.BinOp]
) -> Iterator[ast.BinOp]:
    values = {}
    op_values = {ast.BitXor: 0, ast.BitAnd: 1, ast.BitOr: 2}

    def calc(target: str):
        if target in names:
            if target in names:
                return ast.Name(target), 0
            return values[target]
        match eqns[target]:
            case ast.BinOp(
                left=ast.Name(a),
                right=ast.Name(b),
            ):
                left, ldepth = calc(a)
                right, rdepth = calc(b)
            case _:
                raise ValueError('Unknown ast')
        if (rdepth, value(right)) < (ldepth, value(left)):
            left, right = right, left
        depth = max(ldepth, rdepth)
        res = ast.BinOp(
            left=left,
            op=eqns[target].op,
            right=right,
        )
        values[target] = res, depth
        return res, depth + 1

    def value(node: ast.AST):
        match node:
            case ast.Name(name):
                return 0, name
            case ast.BinOp(op=op):
                return 1, op_values[type(op)]

    return (c for c, _ in map(calc, targets)), values


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

    print(part_a_solver(*data[:-1]))
    print(part_b_solver(*data[:-1]))
