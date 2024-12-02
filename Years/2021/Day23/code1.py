import heapq
from typing import Any, NamedTuple

from Years.path_stuff import *

reverse_symbol_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
amphipod_energy_dict = {0: 1, 1: 10, 2: 100, 3: 1000}
hall_dict = {0: 0, 1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 10}
accessibility_dict = {(1, 1): (0, 1), (1, 2): (0, 2), (1, 3): (0, 3),
                      (2, 2): (1, 2), (2, 3): (1, 3),
                      (3, 0): (0, 1), (3, 3): (2, 3),
                      (4, 0): (0, 2), (4, 1): (1, 2),
                      (5, 0): (0, 3), (5, 1): (1, 3), (5, 2): (2, 3)}


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        match len(inputs):
            case 0:
                file_to_read = test_path
            case 1:
                return inputs[0]
            case _:
                return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        rtn = []
        symbol_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        for line in file.read().splitlines()[2:4]:
            rtn.append(line[3:10].split('#'))
        # Turns locations into a Node object
        return Node(*((complex(1, i[2]), complex(1, j[2] + 4)) for i, j in
                      zip(*[iter(sorted((symbol_dict[v], row, room)
                                        for row, j in enumerate(rtn)
                                        for room, v in enumerate(j)))] * 2)))


def comp_to_2tuple(num: complex) -> tuple[int, int]:
    return int(num.real), int(num.imag)


class Node(NamedTuple):
    a: tuple[complex, complex]
    b: tuple[complex, complex]
    c: tuple[complex, complex]
    d: tuple[complex, complex]

    @staticmethod
    def is_in_place(amp_type: int, loc: complex) -> bool:
        return loc.real and loc.imag % 4 == amp_type

    def is_blocking(self, amp_type: int, loc: complex) -> bool:
        if (row := loc.imag) not in (0, 1, 2, 3):
            return False
        for i, j in self[:amp_type] + self[amp_type + 1:]:
            if (i.real and i.imag - 4 == row) or (j.real and j.imag - 4 == row):
                return True
        return False

    def is_blocked(self, amp_type: int, loc: complex) -> bool:
        if (row := loc.imag) not in (4, 5, 6, 7):
            return False
        for i, j in self[:amp_type] + self[amp_type + 1:]:
            if (i.real and i.imag + 4 == row) or (j.real and j.imag + 4 == row):
                return True
        return False

    def is_empty(self, loc: complex) -> bool:
        return not (loc in (j for i in self for j in i))

    def is_end(self) -> bool:
        return all(self.is_in_place(amp_type, i) for amp_type, v in enumerate(self) for i in v)

    def get_amp_type(self, loc: complex) -> int:
        # Assuming an amphipod is at loc
        for i, v in enumerate(self):
            if loc in v:
                return i
        raise NotImplementedError('self.get_amp_type called when amphipod is not at loc')

    def get_movable_amphipods(self) -> list[tuple[int, int], ...]:
        movable_amphipods: list[tuple[int, int]] = []
        for amp_type, j in enumerate(self):
            for i, v in enumerate(j):
                match comp_to_2tuple(v):
                    case 0, hall:
                        if hall == 0:
                            if self.is_empty(1j):
                                movable_amphipods.append((amp_type, i))
                        elif hall == 6:
                            if self.is_empty(5j):
                                movable_amphipods.append((amp_type, i))
                        else:
                            movable_amphipods.append((amp_type, i))
                    case 1, row if row in (0, 1, 2, 3):
                        if not self.is_in_place(amp_type, v) or self.is_blocking(amp_type, v):
                            movable_amphipods.append((amp_type, i))
                    case 1, _:
                        if not self.is_in_place(amp_type, v) and not self.is_blocked(amp_type, v):
                            movable_amphipods.append((amp_type, i))
                    case idk:
                        print(f'{idk=}')
                        raise NotImplementedError
        return movable_amphipods

    def get_free_hall_spaces(self, loc: complex) -> list[complex]:
        if not loc.real:
            raise NotImplementedError
        splits = [not self.is_empty(i) for i in (2j, 3j, 4j)]
        room = loc.imag % 4
        hall_spaces = [num for i in range(1, 6) if self.is_empty(num := complex(0, i)) and
                       not any(splits[slice(*accessibility_dict.get((i, room), (0,)))])]
        if 1j in hall_spaces and self.is_empty(0j):
            hall_spaces.append(0j)
        if 5j in hall_spaces and self.is_empty(6j):
            hall_spaces.append(6j)
        return hall_spaces

    def get_room_accessible(self, amp_type: int, loc: complex) -> complex | bool:
        move_to_back: bool = False
        if not self.is_empty(complex(1, amp_type)):
            return False
        back_row = complex(1, amp_type + 4)
        if self.is_empty(back_row):
            move_to_back = True
        elif not self.is_in_place(self.get_amp_type(back_row), back_row):
            return False
        splits = [not self.is_empty(i) for i in (2j, 3j, 4j)]
        match comp_to_2tuple(loc):
            case 0, hall:
                if not any(splits[slice(*accessibility_dict.get((min(max(hall, 1), 5), amp_type), (0,)))]):
                    return complex(1, amp_type + 4 * move_to_back)
            case 1, room:
                if not any(splits[slice(*sorted((amp_type, room % 4)))]):
                    return complex(1, amp_type + 4 * move_to_back)
            case idk:
                print(f'{idk=}')
                raise NotImplementedError
        return False

    def amphipod_move(self, loc_idx: tuple[int, int], new_loc: complex):
        return Node(*(tuple(new_loc if (amp_type, i) == loc_idx else j for i, j in enumerate(v))
                      for amp_type, v in enumerate(self)))

    def display(self) -> str:
        global reverse_symbol_dict, hall_dict
        hallway = {}
        front = {}
        back = {}
        for amp_type, loc in ((i, j) for i, v in enumerate(self) for j in v):
            match comp_to_2tuple(loc):
                case 0, hall:
                    hallway[hall_dict[hall]] = reverse_symbol_dict[amp_type]
                case 1, row if row in (0, 1, 2, 3):
                    front[row] = reverse_symbol_dict[amp_type]
                case 1, row:
                    back[row - 4] = reverse_symbol_dict[amp_type]
                case idk:
                    print(f'{idk=}')
                    raise NotImplementedError
        return f'#{"".join(hallway.get(i, ".") for i in range(11))}#\n' \
               f'###{"#".join(front.get(i, ".") for i in range(4))}###\n' \
               f'###{"#".join(back.get(i, ".") for i in range(4))}###'


# def get_neighbour_nodes_and_weights(energy: int,
#                                     node: Node,
#                                     path: tuple[Node]) -> list[tuple[int, Node, tuple[Node]]:
def get_neighbour_nodes_and_weights(energy: int, node: Node) -> list[tuple[int, Node]]:
    rtn_nodes = []
    # path += (node,)
    for amp_type, idx in node.get_movable_amphipods():
        loc = node[amp_type][idx]
        if room := node.get_room_accessible(amp_type, loc):
            rtn_nodes.append(
                # (energy + get_energy(amp_type, loc, room), node.amphipod_move((amp_type, idx), room), path))
                (energy + get_energy(amp_type, loc, room), node.amphipod_move((amp_type, idx), room)))
        elif loc.real:
            for hall in node.get_free_hall_spaces(loc):
                rtn_nodes.append(
                    # (energy + get_energy(amp_type, loc, hall), node.amphipod_move((amp_type, idx), hall), path))
                    (energy + get_energy(amp_type, loc, hall), node.amphipod_move((amp_type, idx), hall)))
    return rtn_nodes


def get_hallway_distance(room: int, hall: int) -> int:
    global hall_dict
    return abs((2 + 2 * room - hall_dict[hall]))


def get_energy(amp_type: int, start_idx: complex, end_idx: complex) -> int:
    global amphipod_energy_dict
    multiplier = amphipod_energy_dict[amp_type]
    match comp_to_2tuple(start_idx), comp_to_2tuple(end_idx):
        case (1, room), (0, hall):
            steps = room // 4 + 1 + get_hallway_distance(room % 4, hall)
        case (1, start_room), (1, end_room):
            steps = start_room // 4 + end_room // 4 + 2 + 2 * abs((end_room % 4) - (start_room % 4))
        case (0, hall), (1, room):
            steps = room // 4 + 1 + get_hallway_distance(room % 4, hall)
        case _:
            raise NotImplementedError
    return steps * multiplier


def solver(node: Node) -> Any:
    visited = set()
    # active = [(0, 0, node, tuple())]
    active = [(0, 0, node)]
    heapq.heapify(active)
    counter = 0
    print(node)
    while True:
        # energy, _, node, path = heapq.heappop(active)
        energy, _, node = heapq.heappop(active)
        print(energy)
        if node.is_end():
            # path += (node,)
            # print(*(i.display() for i in path), sep='\n\n')
            return energy
        if node in visited:
            continue
        visited.add(node)
        # for new_energy, new_node, new_path in get_neighbour_nodes_and_weights(energy, node, path):
        for new_energy, new_node in get_neighbour_nodes_and_weights(energy, node):
            counter += 1
            # heapq.heappush(active, (new_energy, counter, new_node, new_path))
            heapq.heappush(active, (new_energy, counter, new_node))


def display(energy) -> None:
    print(energy)


if __name__ == '__main__':
    answer = solver(parser(
        Node(a=(0j, 1j), b=((1+2j), (1+4j)), c=((1+0j), (1+7j)), d=((1+3j), (1+6j)))
        , file_name='input.txt',
        testing=True))
    display(answer)
