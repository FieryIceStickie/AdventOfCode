import heapq
from functools import lru_cache
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


def parser(testing_input: Any, file_name: str = '', is_testing: bool = False) -> Any:
    if is_testing:
        if testing_input is None:
            file_to_read = test_path
        else:
            return testing_input
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        rtn = []
        symbol_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        for line in file.read().splitlines()[2:4]:
            rtn.append(line[3:10].split('#'))
        rtn = [rtn[0], ['D', 'C', 'B', 'A'], ['D', 'B', 'A', 'C'], rtn[1]]
        # Turns locations into a Node object
        return Node(*(tuple(complex(1, v[2] + 4 * i) for i, v in enumerate(j)) for j in
                      zip(*[iter(sorted((symbol_dict[v], row, room)
                                        for row, j in enumerate(rtn)
                                        for room, v in enumerate(j)))] * 4)))


def comp_to_2tuple(num: complex) -> tuple[int, int]:
    return int(num.real), int(num.imag)


class Node(NamedTuple):
    a: tuple[complex, complex, complex, complex]
    b: tuple[complex, complex, complex, complex]
    c: tuple[complex, complex, complex, complex]
    d: tuple[complex, complex, complex, complex]

    @staticmethod
    @lru_cache(maxsize=None)
    def is_in_place(amp_type: int, loc: complex) -> bool:
        return loc.real and loc.imag % 4 == amp_type

    def is_blocking(self, loc: complex) -> bool:
        if (row := int(loc.imag)) in (12, 13, 14, 15):
            return False
        for i in range(row + 4, 16, 4):
            if not self.is_empty(block_loc := complex(1, i)):
                if not self.is_in_place(self.get_amp_type(block_loc), block_loc):
                    return True
        return False

    def is_blocked(self, loc: complex) -> bool:
        if (row := int(loc.imag)) in (0, 1, 2, 3):
            return False
        for i in range(row % 4, row, 4):
            if not self.is_empty(complex(1, i)):
                return True
        return False

    def is_empty(self, loc: complex) -> bool:
        return not any(loc in i for i in self)

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
                        if not self.is_in_place(amp_type, v) or self.is_blocking(v):
                            movable_amphipods.append((amp_type, i))
                    case 1, row if row in (12, 13, 14, 15):
                        if not self.is_in_place(amp_type, v) and not self.is_blocked(v):
                            movable_amphipods.append((amp_type, i))
                    case 1, _:
                        if (not self.is_in_place(amp_type, v) or self.is_blocking(v)) \
                                and not self.is_blocked(v):
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
        if not self.is_empty(complex(1, amp_type)):
            return False
        for i in range(3, -1, -1):
            row_loc = complex(1, amp_type + 4 * i)
            if self.is_empty(row_loc) and not self.is_blocked(row_loc) and not self.is_blocking(row_loc):
                row = i
                break
        else:
            return False
        splits = [not self.is_empty(i) for i in (2j, 3j, 4j)]
        match comp_to_2tuple(loc):
            case 0, hall:
                if not any(splits[slice(*accessibility_dict.get((min(max(hall, 1), 5), amp_type), (0,)))]):
                    return complex(1, amp_type + 4 * row)
            case 1, room:
                if not any(splits[slice(*sorted((amp_type, room % 4)))]):
                    return complex(1, amp_type + 4 * row)
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
        front_back = {}
        back_front = {}
        back = {}
        for amp_type, loc in ((i, j) for i, v in enumerate(self) for j in v):
            match comp_to_2tuple(loc):
                case 0, hall:
                    hallway[hall_dict[hall]] = reverse_symbol_dict[amp_type]
                case 1, row if row in (0, 1, 2, 3):
                    front[row] = reverse_symbol_dict[amp_type]
                case 1, row if row in (4, 5, 6, 7):
                    front_back[row - 4] = reverse_symbol_dict[amp_type]
                case 1, row if row in (8, 9, 10, 11):
                    back_front[row - 8] = reverse_symbol_dict[amp_type]
                case 1, row:
                    back[row - 12] = reverse_symbol_dict[amp_type]
                case idk:
                    print(f'{idk=}')
                    raise NotImplementedError
        return f'#{"".join(hallway.get(i, ".") for i in range(11))}#\n' \
               f'###{"#".join(front.get(i, ".") for i in range(4))}###\n' \
               f'###{"#".join(front_back.get(i, ".") for i in range(4))}###\n' \
               f'###{"#".join(back_front.get(i, ".") for i in range(4))}###\n' \
               f'###{"#".join(back.get(i, ".") for i in range(4))}###'


def get_neighbour_nodes_and_weights(energy: int, node: Node, path: tuple[Node]) -> list[tuple[int, Node, tuple[Node]]]:
    rtn_nodes = []
    path += (node,)
    for amp_type, idx in node.get_movable_amphipods():
        loc = node[amp_type][idx]
        if room := node.get_room_accessible(amp_type, loc):
            rtn_nodes.append(
                (energy + get_energy(amp_type, loc, room), node.amphipod_move((amp_type, idx), room), path))
        elif loc.real:
            for hall in node.get_free_hall_spaces(loc):
                rtn_nodes.append(
                    (energy + get_energy(amp_type, loc, hall), node.amphipod_move((amp_type, idx), hall), path))
    return rtn_nodes


def get_hallway_distance(room: int, hall: int) -> int:
    global hall_dict
    return abs((2 + 2 * room - hall_dict[hall]))


@lru_cache(maxsize=None)
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
    active = [(0, 0, node, tuple())]
    heapq.heapify(active)
    counter = 0
    print(f'Starting node:\n{node.display()}\n\n')
    while True:
        energy, _, node, path = heapq.heappop(active)
        if energy > 40000 and node.is_end():
            path += (node,)
            print(*(i.display() for i in path), sep='\n\n')
            return energy
        if node in visited:
            continue
        visited.add(node)
        for new_energy, new_node, new_path in get_neighbour_nodes_and_weights(energy, node, path):
            counter += 1
            heapq.heappush(active, (new_energy, counter, new_node, new_path))


def display(energy) -> None:
    print(energy)


if __name__ == '__main__':
    profiling = False
    # test_input = Node(
    #     a=((1+0j), (1+4j), (1+8j), (1+12j)),
    #     b=((1+1j), (1+5j), (1+9j), (1+13j)),
    #     c=((1+2j), (1+6j), (1+10j), (1+14j)),
    #     d=((1+3j), (1+7j), (1+11j), (1+15j)))
    test_input = Node(
        a=((1+15j), 0j, 1j, (1+12j)),
        b=((1+0j), 5j, 4j, 3j),
        c=((1+11j), (1+6j), (1+10j), (1+14j)),
        d=(6j, (1+8j), (1+4j), (1+13j)))
    testing = False
    if profiling:
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            answer = solver(parser(test_input,
                                   file_name='input.txt',
                                   is_testing=testing))
            display(answer)

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename='profiling.prof')
    else:
        answer = solver(parser(test_input,
                               file_name='input.txt',
                               is_testing=testing))
        display(answer)
