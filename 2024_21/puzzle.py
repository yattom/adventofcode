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

dp = DebugPrinter(enabled=True)

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


@dataclass
class State:
    robot_at_numpad: Pos = Pos(2, 3)
    robot_at_keypad1: Pos = Pos(2, 0)
    robot_at_keypad2: Pos = Pos(2, 0)
    sequence_for_you: str = ''

    def __repr__(self):
        return f'r{self.robot_at_numpad} 1{self.robot_at_keypad1} 2{self.robot_at_keypad2}'


def shortest_sequence(start: Pos, target: Pos, target_pad: Pad) -> str:
    # going zigzag will always cost more
    # assume there's no preference for going vertical or horizontal first
    # we need to avoid GAP
    dx, dy = target.x - start.x, target.y - start.y
    seq = ''
    if dx == 0 or start.y == target_pad[GAP].y:
        # vertical first
        seq += go_vertical(dy)
        seq += go_horizontal(dx)
    else:
        # horizontal first
        seq += go_horizontal(dx)
        seq += go_vertical(dy)
    seq += 'A'
    return seq


def shortest_sequence_set(start: Pos, target: Pos, target_pad: Pad) -> set[str]:
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
        seq_set.add(go_vertical(dy) + go_horizontal(dx) )
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


def calculate_sequence(robot: Pos, target: Pos, target_pad: Pad) -> str:
    seq = shortest_sequence(start=robot, target=target, target_pad=target_pad)
    return seq


def calculate_sequence_for_robot_on_keypad1(state: State, target: Pos) -> str:
    dp.print(f'{state=}')
    seq_on_keypad1 = calculate_sequence(state.robot_at_numpad, target, NUMPAD)
    state.robot_at_numpad = target
    dp.print(f'key={get_label(NUMPAD, target)} {seq_on_keypad1=} {state=}')
    return seq_on_keypad1


def calculate_sequence_for_robot_on_keypad2(state: State, target: Pos) -> str:
    dp.print(f'  {state=}')
    seq_on_keypad2 = calculate_sequence(state.robot_at_keypad1, target, KEYPAD)
    state.robot_at_keypad1 = target
    dp.print(f'  key={get_label(KEYPAD, target)} {seq_on_keypad2=} {state=}')
    return seq_on_keypad2


def calculate_sequence_for_you(state: State, target: Pos) -> str:
    dp.print(f'    {state=}')
    seq_for_you = calculate_sequence(state.robot_at_keypad2, target, KEYPAD)
    state.robot_at_keypad2 = target
    dp.print(f'    key={get_label(KEYPAD, target)} {seq_for_you=} {state=}')
    return seq_for_you


def push_button_numpad(state: State, button: str):
    target_for_robot_on_numpad = NUMPAD[button]
    seq_on_keypad1 = calculate_sequence_for_robot_on_keypad1(state, target_for_robot_on_numpad)
    for c in seq_on_keypad1:
        target_for_robot_on_keypad1 = KEYPAD[c]
        seq_on_keypad2 = calculate_sequence_for_robot_on_keypad2(state, target_for_robot_on_keypad1)
        for d in seq_on_keypad2:
            target_for_robot_on_keypad2 = KEYPAD[d]
            seq_for_you = calculate_sequence_for_you(state, target_for_robot_on_keypad2)
            state.sequence_for_you += seq_for_you


def puzzle1(lines: list[str]):
    score = 0
    for l in lines:
        state = State()
        for c in l.strip():
            push_button_numpad(state, c)
        dp.print(state.sequence_for_you)

        num = int(re.match(r'0*(\d+).*', l.strip()).group(1))
        score += num * len(state.sequence_for_you)
        print(num, len(state.sequence_for_you), num * len(state.sequence_for_you))

    return score


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
