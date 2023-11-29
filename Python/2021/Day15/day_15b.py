from typing import Any, TypeVar

import networkx as nx

T = TypeVar('T', list, str)


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = 'test.txt'
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        lines = file.read().splitlines()
        end = (5 * len(lines) - 1) * complex(1, 1)
        return {complex(i, j): int(r) for i, l in enumerate(expand(lines)) for j, r in enumerate(expand(l))}, end


def expand(iterable: T) -> T:
    if isinstance(iterable, list):
        return sum([[''.join([str(((int(iii) + i - 1) % 9) + 1) for iii in ii])
                     for ii in iterable] for i in range(5)], [])
    elif isinstance(iterable, str):
        return ''.join(sum([[str(((int(i) + j - 1) % 9) + 1) for i in iterable] for j in range(5)], []))
    else:
        raise TypeError


def solver(risk_dict: dict[complex, int], end: complex) -> Any:
    # Not my solution, credit to xelf from python discord whom I stole this code from

    def get_neighbours(z: complex):
        return (z + d for d in (1, 1j, -1, -1j) if z + d in risk_dict)

    graph = nx.DiGraph(((pt, npt, {'weight': risk_dict[npt]}) for pt in risk_dict for npt in get_neighbours(pt)))
    return nx.dijkstra_path_length(graph, 0j, end, weight='weight')


def display(risk) -> None:
    print(risk)


if __name__ == '__main__':
    answer = solver(*parser(
        file_name='day_15.txt',
        testing=False))
    display(answer)
