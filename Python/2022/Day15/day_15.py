import re
from Tools.utils import display_visited
from typing import Self, NamedTuple
from collections import Counter
from itertools import combinations, product

def parser(filename: str) -> tuple[list, list]:
    with open(filename, 'r') as file:
        sensor_beacon_locs = [v for *v, in (map(int, re.findall(r'=(-?\d+)', row)) for row in file.read().splitlines())]
        return [(sx, sy, abs(sx - bx) + abs(sy - by)) for sx, sy, bx, by in sensor_beacon_locs], \
            [(bx, by) for _, _, bx, by in sensor_beacon_locs]


class SensorRange(NamedTuple):
    min: int
    max: int
    def sum(self, *others) -> Self:
        return SensorRange(min((self.min, *(i.min for i in others))), max((self.max, *(i.max for i in others))))
    def is_intersect(self, other) -> bool:
        return max(self.min, other.min) <= min(self.max, other.max)
    def restrict(self, max_val: int):
        return SensorRange(max(0, self.min), min(max_val, self.max))
    def __len__(self):
        return self.max - self.min + 1


class Point(NamedTuple):
    x: int
    y: int
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def __floordiv__(self, other):
        return Point(self.x // other, self.y // other)
    def __len__(self):
        return abs(self.x) + abs(self.y)



class Segment(NamedTuple):
    p1: Point
    p2: Point
    @property
    def parity(self) -> -1 | 1:
        return self.p1.y > self.p2.y

    @classmethod
    def order(cls, p1, p2):
        return cls(*sorted((p1, p2)))

    def __contains__(self, item: Point):
        return self.p1.x <= item.x <= self.p2.x and item.y - self.p1.y == -self.parity * (item.x - self.p1.x)
    def is_intersect(self, other):
        if self.parity == other.parity:
            return max(self.p1, other.p1) <= min(self.p2, other.p2)
        intersection = self.get_intersection(other)
        return intersection in self and intersection in other

    def get_intersection(self, other):
        (a, b), _ = sorted((self, other), key=lambda s: s.parity)
        a, b, c, d = a.x, a.y, b.x, b.y
        return Point((-a + b + c + d) // 2, (a - b + c + d) // 2)
class Rhombus(NamedTuple):
    top: Point
    right: Point
    bottom: Point
    left: Point
    @property
    def centre(self):
        return (self.left + self.right) // 2

    @property
    def radius(self):
        return len(self.right - self.centre)
    def __contains__(self, item: Point):
        return len(item - self.centre) <= self.radius

    @classmethod
    def from_srange(cls, sensor: Point, r: int):
        deltas = (Point(x, y) for x, y in ((0, -r), (r, 0), (0, r), (-r, 0)))
        return cls(*(sensor + d for d in deltas))

    def segments(self) -> tuple[Segment, ...]:
        return Segment(self.top, self.right), Segment(self.bottom, self.right), \
            Segment(self.left, self.bottom), Segment(self.left, self.top)

def part_a_solver(row_y: int, sensor_ranges: list[tuple[int, int, int]], beacon_locs: list[tuple[int, int]]):
    ranges = set()
    for x, y, r in sensor_ranges:
        if (d := r - abs(y - row_y)) > 0:
            srange = SensorRange(x-d, x+d)
            intersections = {i for i in ranges if i.is_intersect(srange)}
            ranges -= intersections
            ranges.add(srange.sum(*intersections))
    return sum(len(i) for i in ranges) - len({x for x, y in beacon_locs if y == row_y})

def part_b_solver(sensor_ranges: list[tuple[int, int, int]]):
    cmax = 4000000
    lines = [((x+y-r-1, 1),(-x+y-r-1,-1),(x+y+r+1, 1),(-x+y+r+1, -1)) for x, y, r in sensor_ranges]
    candidates = set()
    for a, b, c, d in combinations(lines, 4):
        for i, j, k, l in product(a, b, c, d):
            if (i[1] == j[1])^(i[1] == k[1])^(i[1] == l[1]):
                i, j, k, l = sorted((i, j, k, l), key=lambda p: p[1])
                if i != j or k != l:
                    continue
                i1 = ((k[0]-i[0])//2, (k[0]+i[0])//2)
                if not (0 <= i1[0] <= cmax and 0 <= i1[1] <= cmax):
                    continue
                candidates.add(i1)
                break
    for i in candidates:
        check = True
        for x, y, r in sensor_ranges:
            if abs(i[0]-x)+abs(i[1]-y) <= r:
                check = False
                break
        if check:
            return i[0] * 4000000 + i[1]
    raise ValueError


if __name__ == '__main__':
    inputs = parser('day_15.txt')
    print(part_a_solver(2000000, *inputs))
    # print(part_b_solver(inputs[0]))