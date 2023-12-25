from typing import TextIO

from Python.path_stuff import *
import networkx as nx
from math import prod
from functools import partial

ssplit = lambda s: partial(str.split, sep=s)


def parser(raw_data: TextIO) -> nx.Graph:
    return nx.Graph(
        (node1, node2)
        for node1, nodes in map(ssplit(': '), raw_data.read().splitlines())
        for node2 in nodes.split()
    )


def solver(graph: nx.Graph) -> int:
    return graph.remove_edges_from(nx.minimum_edge_cut(graph)) or prod(map(len, nx.connected_components(graph)))


if __name__ == '__main__':
    testing = False

    with open(test_path if testing else 'input.txt', 'r') as file:
        data = parser(file)

    print(solver(data))
