import re
import time
from copy import copy
from dataclasses import dataclass
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
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, pos: Pos):
        x, y = pos
        if not self.is_point_on_grid(pos):
            return ''
        return self.grid[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        self.grid[y][x] = value

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


dp = DebugPrinter(enabled=False)


def puzzle1(lines: list[str]):
    locks = []
    keys = []
    for i in range(0, len(lines), 8):
        schema_str = [l.strip() for l in lines[i:i+7]]
        assert i + 7 >= len(lines) or lines[i + 7].strip() == ''
        if schema_str[0] == '#####':
            # lock
            lock = []
            for x in range(len(schema_str[1])):
                for y in range(1, len(schema_str)):
                    if schema_str[y][x] != '#':
                        lock.append(y - 1)
                        break

            print(f'{lock=}')
            locks.append(lock)
        elif  schema_str[6] == '#####':
            # key
            key = []
            for x in range(len(schema_str[1])):
                for y in range(len(schema_str)-1, -1, -1):
                    if schema_str[y][x] != '#':
                        key.append(5 - y)
                        break
            print(f'{key=}')
            keys.append(key)
        else:
            raise ValueError('Invalid schema')

    matches = 0
    for k in keys:
        for l in locks:
            if all(kv + lv <= 5 for kv, lv in zip(k, l)):
                matches +=1
    return matches


def puzzle2(lines: list[str]):
    return 0


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
