import re
import time
from copy import copy
from dataclasses import dataclass, field
from typing import TypeAlias


class DebugPrinter:
    def __init__(self, enabled=False, interval=0):
        self.enabled = enabled
        self.interval = interval
        if self.interval:
            self.start_ns = time.time_ns()
            self.last_ns = self.start_ns

    def print(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)

    def at_interval(self) -> bool:
        if not self.enabled or not self.interval:
            return False
        if time.time_ns() - self.last_ns > self.interval:
            self.last_ns += self.interval
            return True

    def elapsed(self):
        return (time.time_ns() - self.start_ns) / (1000 * 1000 * 1000)


DIRECTION = {
    (0, -1): '^',
    (0, 1): 'v',
    (-1, 0): '<',
    (1, 0): '>',
}


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


class Grid:
    NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, grid: list[list[str]]):
        self.grid = [[c for c in l.strip()] for l in grid]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __getitem__(self, pos: Pos):
        if not self.is_point_on_grid(pos):
            return ''
        return self.grid[pos.y][pos.x]

    def __setitem__(self, pos, value):
        self.grid[pos.y][pos.x] = value

    def __copy__(self):
        return Grid([row[:] for row in self.grid])

    def is_point_on_grid(self, pos: Pos):
        x, y = pos.x, pos.y
        return 0 <= x < self.width and 0 <= y < self.height

    def find(self, char: str) -> Pos | None:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    return Pos(x, y)
        return None

    def find_all(self, char: str) -> list[Pos]:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    yield Pos(x, y)

    def dump(self, marks: dict[Pos, str] = None):
        print('-' * 10)
        for y, row in enumerate(self.grid):
            s = ''
            for x, c in enumerate(row):
                if marks and Pos(x, y) in marks:
                    s += marks[Pos(x, y)]
                else:
                    s += c
            print(s)
        print()

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                yield Pos(x, y), c


def memoize(func):
    memo = {}

    def wrapper(*args, **kwargs):
        key = (repr(args), repr(kwargs.items()))
        if key not in memo:
            memo[key] = func(*args, **kwargs)
        return copy(memo[key])

    return wrapper


dp = DebugPrinter(enabled=True)


class TestTreeOfRange:
    def test_concrete_range(self):
        cr3_5 = TreeOfRange.ConcreteRange(3, 5)
        assert 3 in cr3_5
        assert 5 in cr3_5
        assert 2 not in cr3_5
        assert 6 not in cr3_5

    def test_single(self):
        sut = TreeOfRange()
        sut.add(1, 3)
        assert 1, 3 == (sut.lower, sut.higher)

    def test_two(self):
        sut = TreeOfRange()
        sut.add(1, 3)
        sut.add(5, 8)
        assert 1, 8 == (sut.lower, sut.higher)
        assert len(sut.nodes) == 2

    def test_two_reverse(self):
        sut = TreeOfRange()
        sut.add(5, 8)
        sut.add(1, 3)
        assert 1, 8 == (sut.lower, sut.higher)

    def test_two_levels(self):
        sut = TreeOfRange()
        sut.add(1, 3)
        sut.add(5, 8)
        sut.add(0, 2)
        sut.add(4, 6)
        sut.add(6, 7)
        sut.add(10, 10)
        assert 1, 12 == (sut.lower, sut.higher)
        assert len(sut.nodes) == 2
        assert -1 not in sut
        assert 0 in sut
        assert 1 in sut
        assert 3 in sut
        assert 9 not in sut
        assert 10 in sut
        assert 11 not in sut


class TreeOfRange:
    @dataclass
    class ConcreteRange:
        lower: int
        higher: int

        def __contains__(self, n: int):
            return self.lower <= n <= self.higher

        def __repr__(self):
            return f'[{self.lower},{self.higher}]'

    def __init__(self):
        self.nodes = []
        self.lower = self.higher = None

    def __contains__(self, n: int):
        if n < self.lower or self.higher < n:
            return False
        for node in self.nodes:
            if n in node:
                return True
        return False

    def __repr__(self):
        return f'T({self.nodes}, lo={self.lower}, hi={self.higher})'

    def recalc(self):
        self.lower = min((n.lower for n in self.nodes))
        self.higher = max((n.higher for n in self.nodes))

    def add(self, lower, higher):
        new_cr = TreeOfRange.ConcreteRange(lower, higher)

        if len(self.nodes) == 0:
            self.nodes.append(new_cr)
        elif len(self.nodes) == 1:
            if new_cr.lower < self.nodes[0].lower:
                self.nodes.insert(0, new_cr)
            else:
                self.nodes.append(new_cr)
        elif len(self.nodes) == 2:
            if new_cr.lower < self.nodes[1].lower:
                if type(self.nodes[0]) is TreeOfRange.ConcreteRange:
                    new_tor = TreeOfRange()
                    new_tor.add(self.nodes[0].lower, self.nodes[0].higher)
                    self.nodes[0] = new_tor
                self.nodes[0].add(new_cr.lower, new_cr.higher)
            else:
                if type(self.nodes[1]) is TreeOfRange.ConcreteRange:
                    new_tor = TreeOfRange()
                    new_tor.add(self.nodes[1].lower, self.nodes[1].higher)
                    self.nodes[1] = new_tor
                self.nodes[1].add(new_cr.lower, new_cr.higher)
        else:
            raise RuntimeError(f'illegal nodes: {self.nodes}')
        self.recalc()


def puzzle1(lines: list[str]):
    ranges = TreeOfRange()

    lines_iter = iter(lines)
    for l in lines_iter:
        if l.strip() == '':
            break
        s, e = l.split('-')
        ranges.add(int(s), int(e))

    dp.print(ranges)

    fresh_count = 0
    for l in lines_iter:
        if l.strip() == '':
            continue
        if int(l.strip()) in ranges:
            fresh_count += 1

    return fresh_count


def add_range(ranges, r):
    dp.print(ranges, r)
    for i, rr in enumerate(ranges):
        if r.lower <= rr.higher and rr.lower <= r.higher:
            combined_r = TreeOfRange.ConcreteRange(
                    min([r.lower, rr.lower]),
                    max([r.higher, rr.higher]))
            ranges.pop(i)
            add_range(ranges, combined_r)
            break
    else:
        ranges.append(r)


def puzzle2(lines: list[str]):
    ranges = []

    lines_iter = iter(lines)
    for l in lines_iter:
        if l.strip() == '':
            break
        lower, higher = l.split('-')
        r = TreeOfRange.ConcreteRange(int(lower), int(higher))

        add_range(ranges, r)
        dp.print(ranges)

    total = 0
    for r in ranges:
        total += r.higher - r.lower + 1

    return total


def main():
    import sys
    if len(sys.argv) == 1:
        lines = sys.stdin.readlines()
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    print(puzzle1(lines))
    print(puzzle2(lines))


if __name__ == "__main__":
    main()
