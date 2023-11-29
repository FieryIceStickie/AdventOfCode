from typing import Any
import ast
import operator
from functools import reduce


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = 'test.txt'
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        return [ShellfishNumber(shellfish_list=ast.literal_eval(i)) for i in file.read().splitlines()]


def shellfish_flatten(num: list | int, index: tuple[int, ...] = tuple()) -> list:
    if isinstance(num, list):
        return [vv for i, v in enumerate(num) for vv in shellfish_flatten(v, index + (i,))]
    else:
        return [(num, index)]


class ShellfishNumber:
    def __init__(self, *, shellfish_list: list = None, shellfish_dict: dict = None):
        if shellfish_list is not None:
            self.shellfish_dict = {i: v for v, i in shellfish_flatten(shellfish_list)}
        elif shellfish_dict is not None:
            self.shellfish_dict = shellfish_dict
        else:
            raise NotImplementedError
        self.index_order: list = sorted(self.shellfish_dict.keys())

    def __add__(self, other):
        new_shellfish_dict = {**{(0,) + i: v for i, v in self.shellfish_dict.items()},
                              **{(1,) + i: v for i, v in other.shellfish_dict.items()}}
        new_shellfish_number = ShellfishNumber(shellfish_dict=new_shellfish_dict)
        new_shellfish_number.reduction()
        return new_shellfish_number

    def reduction(self):
        while (check_result := self.reduced_check())[0]:
            reduction_type, index = check_result[1:]
            if reduction_type:
                self.explode(index)
            else:
                self.split(index)

    def reduced_check(self) -> tuple[bool, None | bool, None | tuple[int, ...]]:
        for idx in self.index_order:
            if len(idx) == 5:
                return True, True, idx[:4]
        for idx in self.index_order:
            if self.shellfish_dict[idx] >= 10:
                return True, False, idx
        return False, None, None

    def explode(self, pair_index: tuple[int, ...]):
        left_index, right_index = pair_index + (0,), pair_index + (1,)
        left_order_index, right_order_index = self.index_order.index(left_index), self.index_order.index(right_index)
        match left_order_index, right_order_index:
            case 0, 1:
                right_neighbour_idx = self.index_order[2]
                self.shellfish_dict[right_neighbour_idx] += self.shellfish_dict[right_index]
            case left_idx, right_idx if right_idx == len(self.index_order) - 1:
                left_neighbour_idx = self.index_order[left_idx - 1]
                self.shellfish_dict[left_neighbour_idx] += self.shellfish_dict[left_index]
            case left_idx, right_idx:
                left_neighbour_idx = self.index_order[left_idx - 1]
                right_neighbour_idx = self.index_order[right_idx + 1]
                self.shellfish_dict[left_neighbour_idx] += self.shellfish_dict[left_index]
                self.shellfish_dict[right_neighbour_idx] += self.shellfish_dict[right_index]
        del self.index_order[left_order_index: right_order_index + 1]
        self.index_order.insert(left_order_index, pair_index)
        del self.shellfish_dict[left_index]
        del self.shellfish_dict[right_index]
        self.shellfish_dict[pair_index] = 0

    def split(self, num_index: tuple[int, ...]):
        num = self.shellfish_dict[num_index]
        order_index = self.index_order.index(num_index)
        left_num, right_num = num // 2, -(num // -2)
        left_index, right_index = num_index + (0,), num_index + (1,)
        del self.shellfish_dict[num_index]
        self.shellfish_dict[left_index] = left_num
        self.shellfish_dict[right_index] = right_num
        del self.index_order[order_index]
        self.index_order.insert(order_index, right_index)
        self.index_order.insert(order_index, left_index)

    def __str__(self) -> str:
        return str(self.shellfish_dict)

    def __eq__(self, other) -> bool:
        if self.index_order == other.index_order:
            return True
        else:
            return False

    def __int__(self) -> int:
        return sum((self.shellfish_dict[idx] * reduce(operator.mul, (2 if i else 3 for i in idx))
                    for idx in self.index_order))


class ShellfishZero:
    def __add__(self, other: ShellfishNumber) -> ShellfishNumber:
        return other


def solver(inputs: Any) -> Any:
    return max([int(x + y) for x in inputs for y in inputs if x != y])


def display(magnitude) -> None:
    print(magnitude)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='day_18.txt',
        testing=False))
    display(answer)
