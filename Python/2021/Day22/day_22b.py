from typing import Any
import cProfile
import pstats
from typing import NamedTuple
import re


class CuboidRange(NamedTuple):
    min: int
    max: int

    def in_range(self, value: int) -> bool:
        return self.min <= value <= self.max

    def is_intersect(self, other) -> bool:
        return self.in_range(other.min) or other.in_range(self.min)

    def find_intersect(self, other):
        _, range_min, range_max, _ = sorted((self.min, self.max, other.min, other.max))
        return CuboidRange(range_min, range_max)

    def size(self) -> int:
        return self.max - self.min + 1

    def __str__(self):
        return f'({self.min}->{self.max})'


class Cuboid(NamedTuple):
    x_range: CuboidRange
    y_range: CuboidRange
    z_range: CuboidRange
    sign: int = 1

    def is_intersect(self, other) -> bool:
        return self.x_range.is_intersect(other.x_range) and \
               self.y_range.is_intersect(other.y_range) and \
               self.z_range.is_intersect(other.z_range)

    def find_intersection_cube(self, other):
        return Cuboid(self.x_range.find_intersect(other.x_range),
                      self.y_range.find_intersect(other.y_range),
                      self.z_range.find_intersect(other.z_range), -other.sign)

    def size(self) -> int:
        return self.sign * self.x_range.size() * self.y_range.size() * self.z_range.size()

    def __neg__(self):
        return Cuboid(self.x_range, self.y_range, self.z_range, -self.sign)

    def __str__(self):
        return f'{"-" if self.sign == -1 else ""}({self.x_range}, {self.y_range}, {self.z_range})'


def parser(*inputs: Any, file_name: str = '', testing: bool = False) -> Any:
    if testing:
        if len(inputs) == 0:
            file_to_read = 'test.txt'
        else:
            return inputs
    else:
        file_to_read = file_name
    with open(file_to_read, 'r') as file:
        instructions = []
        for line in file.read().splitlines():
            state, x_min, x_max, y_min, y_max, z_min, z_max = [int(i) if i not in ('on', 'off') else i == 'on'
                                                               for i in re.match(
                    r'(on|off) x=([-\d]+)..([-\d]+),y=([-\d]+)..([-\d]+),z=([-\d]+)..([-\d]+)', line).groups()]
            instructions.append((state, Cuboid(
                CuboidRange(x_min, x_max), CuboidRange(y_min, y_max), CuboidRange(z_min, z_max))))
        return instructions


def solver(instructions: list[tuple[bool, Cuboid], ...]) -> Any:
    cuboids: list[Cuboid] = []
    for state, new_cuboid in instructions:
        if not state:
            new_cuboid = -new_cuboid
        for cuboid in tuple(cuboids):
            if new_cuboid.is_intersect(cuboid):
                cuboids.append(new_cuboid.find_intersection_cube(cuboid))
        if state:
            cuboids.append(new_cuboid)
    return sum(i.size() for i in cuboids)


def display(count) -> None:
    print(count)


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        answer = solver(parser(
            file_name='day_22.txt',
            testing=False))
        display(answer)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')
