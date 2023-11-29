from typing import Any
from collections import Counter


class Polymer:
    def __init__(self, template: str, insertions: list[str]):
        self.monomers = Counter(template)
        self.insertion_dict = {i: (f'{i[0]}{v}', f'{v}{i[1]}', v) for i, v in (j.split(' -> ') for j in insertions)}
        self.monomer_pairs = Counter([f'{v}{template[i+1]}' for i, v in enumerate(template[:-1])])
        self.count = 0

    def step(self):
        self.count += 1
        added_monomer_pairs = Counter()
        subtracted_monomer_pairs = Counter()
        for i, v in self.monomer_pairs.items():
            first_pair, second_pair, monomer = self.insertion_dict[i]
            added_monomer_pairs += Counter({first_pair: v, second_pair: v})
            subtracted_monomer_pairs += Counter({i: v})
            self.monomers += Counter({monomer: v})
        self.monomer_pairs += added_monomer_pairs
        self.monomer_pairs -= subtracted_monomer_pairs

    def get_max(self) -> int:
        return self.monomers.most_common(1)[0][1]

    def get_min(self) -> int:
        return self.monomers.most_common()[-1][1]


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
        polymer = Polymer(lines[0], lines[2:])
        return polymer


def solver(polymer: Polymer) -> Any:
    for _ in range(40):
        polymer.step()
    return polymer.get_max() - polymer.get_min()


def display(subtraction) -> None:
    print(subtraction)


if __name__ == '__main__':
    answer = solver(parser(
        file_name='day_14.txt',
        testing=False))
    display(answer)
