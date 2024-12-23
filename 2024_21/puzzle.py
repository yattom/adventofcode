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


GAP = 'X'
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


dp = DebugPrinter(enabled=False)

NUMPAD = {
    '7': Pos(0, 0),
    '8': Pos(1, 0),
    '9': Pos(2, 0),
    '4': Pos(0, 1),
    '5': Pos(1, 1),
    '6': Pos(2, 1),
    '1': Pos(0, 2),
    '2': Pos(1, 2),
    '3': Pos(2, 2),
    GAP: Pos(0, 3),
    '0': Pos(1, 3),
    'A': Pos(2, 3),
}
KEYPAD = {
    GAP: Pos(0, 0),
    '^': Pos(1, 0),
    'A': Pos(2, 0),
    '<': Pos(0, 1),
    'v': Pos(1, 1),
    '>': Pos(2, 1),
}

Pad: TypeAlias = dict[str, Pos]


def get_label(pad: Pad, pos):
    for p in pad:
        if pad[p] == pos:
            return p
    return None


def memoize(func):
    memo = {}

    def wrapper(*args, **kwargs):
        key = (repr(args), repr(kwargs.items()))
        if key not in memo:
            memo[key] = func(*args, **kwargs)
        return copy(memo[key])

    return wrapper


@memoize
def get_sequence_set(start: Pos, target: Pos, target_pad: Pad) -> set[str]:
    # going zigzag will always cost more
    # we need to avoid GAP
    dx, dy = target.x - start.x, target.y - start.y
    seq_set = set()

    if start.y == target_pad[GAP].y and target.x == target_pad[GAP].x:
        # skip horizontal first
        pass
    else:
        # horizontal first
        seq_set.add(go_horizontal(dx) + go_vertical(dy))
    if start.x == target_pad[GAP].x and target.y == target_pad[GAP].y:
        # skip vertical first
        pass
    else:
        # horizontal first
        seq_set.add(go_vertical(dy) + go_horizontal(dx))
    assert len(seq_set) == 1 or len(seq_set) == 2, f'wrong length {seq_set=}'
    return set([s + 'A' for s in seq_set])


def go_vertical(dy):
    if dy > 0:
        return 'v' * dy
    else:
        return '^' * (-dy)


def go_horizontal(dx):
    if dx > 0:
        return '>' * dx
    else:
        return '<' * (-dx)


def shortest_sequence_set_for_robot_on_keypad1(robot_on_numpad: Pos, target: Pos) -> set[str]:
    return get_sequence_set(start=robot_on_numpad, target=target, target_pad=NUMPAD)


def shortest_sequence_set_for_robot_on_keypad2(robot_on_keypad1: Pos, target: Pos) -> set[str]:
    return get_sequence_set(start=robot_on_keypad1, target=target, target_pad=KEYPAD)


@memoize
def shortest_sequence_set_for_you(robot_on_numpad: Pos, target: Pos, number_of_robots_on_keypads) -> set[str]:
    seq_on_keypad1 = shortest_sequence_set_for_robot_on_keypad1(robot_on_numpad, target)
    dp.print(f'{len(seq_on_keypad1)=} {seq_on_keypad1=}')

    seq_on_keypad = for_robots(number_of_robots_on_keypads, seq_on_keypad1)
    return seq_on_keypad


@memoize
def for_robots(i, seq):
    if i == 0:
        return seq
    next_seq = sequence_set_for_sequence_on_keypad(seq)
    dp.print(f'{len(next_seq)=} {next_seq=}')
    return for_robots(i - 1, next_seq)


def filter_shortest(seq_set: set[str]) -> set[str]:
    result = set()
    min_len = min(len(seq) for seq in seq_set)
    return set([s for s in seq_set if len(s) == min_len])


@memoize
def sequence_set_for_sequence_on_keypad(sequence_set: set[str]):
    seq_on_keypad = set()
    for s in sequence_set:
        seq = {''}
        target_robot = KEYPAD['A']  # always start from A
        for c in s:
            target_for_robot_on_keypad = KEYPAD[c]
            seq = concat_sequence(seq,
                                  shortest_sequence_set_for_robot_on_keypad2(target_robot, target_for_robot_on_keypad))
            target_robot = target_for_robot_on_keypad
        seq_on_keypad |= seq
    return filter_shortest(seq_on_keypad)


def concat_sequence(heads: set[str], tails: set[str]) -> set[str]:
    if not heads:
        return tails
    if not tails:
        return heads
    result = set()
    for h in heads:
        for t in tails:
            result.add(h + t)
    return result


def solve(lines: list[str], number_of_robots_on_keypads: int):
    score = 0
    for l in lines:
        seq = ''
        robot = NUMPAD['A']
        for c in l.strip():
            seq += shortest_sequence_set_for_you(robot, NUMPAD[c], number_of_robots_on_keypads).pop()
            robot = NUMPAD[c]
        dp.print(seq)

        num = int(re.match(r'0*(\d+).*', l.strip()).group(1))
        score += num * len(seq)
        print(num, len(seq), num * len(seq))

    return score


def puzzle1(lines: list[str]):
    return solve(lines, 2)


def puzzle2(lines: list[str]):
    return solve(lines, 5)


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
