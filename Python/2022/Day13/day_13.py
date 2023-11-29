import ast
from itertools import zip_longest
from typing import Callable, TypeVar, Any

V = TypeVar('V', bound=Any)
N = list["N | int"]


def parser(filename: str):
    with open(filename, 'r') as file:
        return [[ast.literal_eval(s) for s in pair.split('\n')] for pair in file.read().split('\n\n')]


def compare(left: list, right: list) -> -1 | 0 | 1:
    for l, r in zip_longest(left, right, fillvalue=None):
        match l, r:
            case None, None:
                return 0
            case None, _:
                return 1
            case _, None:
                return -1
            case [*l], [*r]:
                v = compare(l, r)
                if not v: continue
                return v
            case [*l], r:
                v = compare(l, [r])
                if not v: continue
                return v
            case l, [*r]:
                v = compare([l], r)
                if not v: continue
                return v
            case l, r:
                if l == r: continue
                return 1 if l < r else -1


def quicksort(arr: list, cmp: Callable[[list, list], bool]):
    if len(arr) < 2:
        return
    pivot = arr[-1]
    lower, upper = [][:], [][:]
    for i in arr[:-1]:
        if cmp(i, pivot):
            lower.append(i)
        else:
            upper.append(i)
    quicksort(lower, cmp)
    quicksort(upper, cmp)
    arr[0:] = lower + [pivot] + upper


def nested_enumerate(num: list | V, index: tuple[int, ...]=()) -> list[tuple[tuple[int, ...], V]]:
    if isinstance(num, list) and num:
        return [vv for i, v in enumerate(num) for vv in nested_enumerate(v, (*index, i))]
    else:
        return [(index, num)]

def convert(index: tuple[int, ...], num: list | int) -> int:
    return sum(v * 69 ** i for i, v in enumerate(index)) + (num or len(index)-9)


def flatten_for_compare(num: list[list | int]) -> list[int]:
    return [convert(i, v) for i, v in nested_enumerate(num)]



def part_a_solver(list_pairs: list[list[list, list]]):
    # return sum(i + 1 for i, v in enumerate(list_pairs) if compare(*v) > 0)
    return sum(i for i, (j, k) in enumerate(list_pairs, 1) if flatten_for_compare(j) < flatten_for_compare(k))


def part_b_solver(list_pairs: list[list[list, list]]):
    # packets = sum(list_pairs, [[[2]], [[6]]])
    # quicksort(packets, lambda x, y: compare(x, y) > 0)
    # return (packets.index([[2]])+1) * (packets.index([[6]])+1)
    packets = sum(list_pairs, [[[2]], [[6]]])
    packets.sort(key=flatten_for_compare)
    return (packets.index([[2]])+1) * (packets.index([[6]])+1)


if __name__ == '__main__':
    inputs = parser('day_13.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
