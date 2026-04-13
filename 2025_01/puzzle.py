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

class Dial:
    MAX = 100
    arrow = 50
    stop_at_zero_count = 0
    click_at_zero_count = 0

    def move1(self, direction, count):
        dp.print(f'{direction=} {count=} {self.arrow=}')
        if direction == 'R':
            if self.arrow + count >= Dial.MAX:
                self.click_at_zero_count += int((self.arrow + count) / Dial.MAX)
            self.arrow = (self.arrow + count) % 100
        elif direction == 'L':
            if self.arrow - count <= 0:
                self.click_at_zero_count -= int((self.arrow - count) / Dial.MAX) - 1
                if self.arrow == 0:
                    self.click_at_zero_count -= 1
            self.arrow = (self.arrow - count) % 100
        else:
            raise ValueError()
        if self.arrow == 0:
            self.stop_at_zero_count += 1
        dp.print(f'{self.arrow=} {self.click_at_zero_count=}')

    def click(self, arrow):
        self.arrow = arrow % Dial.MAX
        if self.arrow == 0:
            self.click_at_zero_count += 1

    def move2(self, direction, count):
        if direction == 'R':
            for i in range(count):
                self.click(self.arrow + 1)
        elif direction == 'L':
            for i in range(count):
                self.click(self.arrow - 1)
        else:
            raise ValueError()
        if self.arrow == 0:
            self.stop_at_zero_count += 1

    move = move1


def puzzle1(lines: list[str]):
    dial = Dial()
    for l in lines:
        d, n = l[0], int(l[1:])
        dial.move(d, n)
    return dial.stop_at_zero_count


def puzzle2(lines: list[str]):
    dial = Dial()
    for l in lines:
        d, n = l[0], int(l[1:])
        dial.move(d, n)
    return dial.click_at_zero_count

def examine(lines: list[str]):
    dial1 = Dial()
    dial2 = Dial()
    log1 = []
    log2 = []
    for i, l in enumerate(lines):
        d, n = l[0], int(l[1:])
        log1.append(f'{i=} {l=} arrow={dial1.arrow} click_at_zero={dial1.click_at_zero_count}')
        dial1.move1(d, n)

        log2.append(f'{i=} {l=} arrow={dial2.arrow} click_at_zero={dial2.click_at_zero_count}')
        dial2.move2(d, n)

        if log1[-1] != log2[-1]:
            print()
            print('diff!')
            print(log1[-3])
            print(log1[-2])
            print(log1[-1])
            print()
            print(log2[-3])
            print(log2[-2])
            print(log2[-1])
            break


def main():
    import sys
    if len(sys.argv) == 1:
        lines = sys.stdin.readlines()
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    print(puzzle1(lines))
    print(puzzle2(lines))
    examine(lines)


if __name__ == "__main__":
    main()
