from typing import Any

from Python.path_stuff import *


class Node:
    def __init__(self, name: str):
        self.name = name
        self.is_end = (name == 'end')
        self.big: bool = name.isupper()
        self.connections: list[Node] = []

    def add_connection(self, other, *, receive=False):
        self.connections.append(other)
        if not receive:
            other.add_connection(self, receive=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class NodeMap:
    def __init__(self, existing_nodes_dict: dict, start_node: Node):
        self.existing_nodes_dict: dict = existing_nodes_dict
        self.start_node = start_node


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = test_path
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        caves = (i.split('-') for i in file.read().splitlines())
        node_names = ['start']
        start_node = Node('start')
        existing_nodes_dict = {}
        for node1_name, node2_name in caves:
            if node1_name not in node_names:
                node1 = Node(node1_name)
                existing_nodes_dict[node1_name] = node1
                node_names.append(node1_name)
            else:
                match node1_name:
                    case 'start':
                        node1 = start_node
                    case name:
                        node1 = existing_nodes_dict[name]
            if node2_name not in node_names:
                node2 = Node(node2_name)
                existing_nodes_dict[node2_name] = node2
                node_names.append(node2_name)
            else:
                match node2_name:
                    case 'start':
                        node2 = start_node
                    case name:
                        node2 = existing_nodes_dict[name]
            node1.add_connection(node2)
        node_map = NodeMap(existing_nodes_dict, start_node)
        return node_map


def solver(node_map: NodeMap) -> Any:
    start_node = node_map.start_node
    return recursive_pathfinder(start_node, (start_node,))


def recursive_pathfinder(node: Node, traversed_nodes: tuple[Node], has_doubled: bool = False) -> int:
    """
    Finds how many paths to the end a particular node has given a list of non-traversable nodes
    :param node: The node
    :param traversed_nodes: A tuple of traversed smol nodes
    :param has_doubled: A boolean representing whether a smol cave has been visited twice
    :return: How many paths
    """
    if node.is_end:
        return 1
    paths_to_explore: list[tuple[Node, int]] = []
    for path in node.connections:
        if str(path) == 'start':
            pass
        elif path.big:
            # Type 0: BIG
            paths_to_explore.append((path, 0))
        elif path not in traversed_nodes:
            # Type 1: Smol never seen
            paths_to_explore.append((path, 1))
        elif not has_doubled:
            # Type 2: Smol seen, but double
            paths_to_explore.append((path, 2))
    routes = 0
    for path, path_type in paths_to_explore:
        new_traversed_nodes = traversed_nodes
        new_has_doubled = has_doubled
        match path_type:
            case 0:
                pass
            case 1:
                new_traversed_nodes += (path,)
            case 2:
                new_has_doubled = True
            case _:
                raise NotImplementedError
        routes += recursive_pathfinder(path, new_traversed_nodes, new_has_doubled)
    return routes


def display(routes) -> None:
    print(routes)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='input.txt',
        testing=False))
    display(answer)
