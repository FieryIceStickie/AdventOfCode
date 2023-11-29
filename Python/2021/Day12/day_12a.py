from typing import Any


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
            file_to_read = 'test.txt'
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
    return recursive_pathfinder(start_node, (start_node, ))


def recursive_pathfinder(node: Node, non_traversable_nodes: tuple) -> int:
    """
    Finds how many paths to the end a particular node has given a list of non-traversable nodes
    :param node: The node
    :param non_traversable_nodes: A tuple of previously traversed nodes
    :return: How many paths
    """
    if node.is_end:
        return 1
    paths_to_explore = [path for path in node.connections if path not in non_traversable_nodes]
    return sum((recursive_pathfinder(path, non_traversable_nodes + ((path,) if not path.big else tuple()))
                for path in paths_to_explore))


def display(routes) -> None:
    print(routes)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='day_12.txt',
        testing=False))
    display(answer)
