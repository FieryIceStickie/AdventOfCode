from typing import Self

from attrs import define, field


@define
class File:
    name: str
    size: int = field(converter=int)


@define
class Directory:
    name: str
    parent: Self
    size: int = 0
    contents: list[File, Self] = field(factory=list)

    def add_to_dir(self, content: File | Self):
        self.contents.append(content)
        self.update_size(content.size)

    def update_size(self, added_size: int):
        self.size += added_size
        if self.parent is not None:
            self.parent.update_size(added_size)

    def __str__(self):
        rtn_str = f'- {self.name} (dir)'
        for i in self.contents:
            match i:
                case Directory() as nested_dir:
                    rtn_str += '\n    ' + nested_dir.__str__().replace('\n', '\n    ')
                case File(filename, size):
                    rtn_str += f'\n    - {filename} (file, size={size})'
        return rtn_str


def parser(filename: str):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def parse_dir(terminal_output: list[str]) -> list[Directory]:
    root = Directory('/', None)
    dirs = [root]
    current_dir = root
    for i in terminal_output:
        match i.split():
            case ['$', 'cd', '/']:
                current_dir = root
            case ['$', 'cd', '..']:
                current_dir = current_dir.parent
            case ['$', 'cd', new_dir]:
                current_dir = next(i for i in current_dir.contents if i.name == new_dir)
            case ['$', 'ls']:
                pass
            case ['dir', new_dir]:
                directory = Directory(new_dir, current_dir)
                current_dir.add_to_dir(directory)
                dirs.append(directory)
            case [size, filename]:
                current_dir.add_to_dir(File(filename, size))
            case idk:
                print(idk)
                raise NotImplemented
    return dirs


def part_a_solver(output: list[str]):
    dirs = parse_dir(output)
    return sum(i.size for i in dirs if i.size <= 100000)


def part_b_solver(output: list[str]):
    dirs = parse_dir(output)
    return next(i.size for i in sorted(dirs, key=lambda x:x.size) if i.size >= dirs[0].size - 40000000)


if __name__ == '__main__':
    inputs = parser('input.txt')
    print(part_a_solver(inputs))
    print(part_b_solver(inputs))
