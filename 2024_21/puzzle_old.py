import time
from dataclasses import dataclass
from typing import TypeAlias

Pos: TypeAlias = tuple[int, int]


class Grid:
    NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, pos):
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
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def find(self, char: str) -> Pos | None:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    return x, y
        return None

    def find_all(self, char: str) -> list[Pos]:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    yield x, y

    def dump(self, marks: dict[Pos, str] = None):
        print('-' * 10)
        for y, row in enumerate(self.grid):
            s = ''
            for x, c in enumerate(row):
                if marks and (x, y) in marks:
                    s += marks[x, y]
                else:
                    s += c
            print(s)
        print()

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                yield (x, y), c


def parse_as_grid(lines: list[str]):
    return Grid([list(line.strip('\n')) for line in lines])


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


NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]

GAP = 'X'

Pad: TypeAlias = dict[str, Pos]


def is_gap(pad: Pad, pos):
    for p in pad:
        if p == GAP and pad[p] == pos:
            return True
    return False


def get_label(pad: Pad, pos):
    for p in pad:
        if pad[p] == pos:
            return p
    return None


DIRECTION = {
    (0, -1): '^',
    (0, 1): 'v',
    (-1, 0): '<',
    (1, 0): '>',
}


def get_sequence_to_push_button(robot, target, pad_for_robot: Pad, pad_to_control: Pad):
    solution = []
    sequence: set[tuple[str, Pos]] = {('', robot)}
    while True:
        new_sequence = set()
        for seq, robot in sequence:
            # print(f'{seq=} {robot=}')
            if robot == target:
                # print(f'SOLUTION {seq=}')
                solution.append(seq)
                continue
            dx = 1 if robot[0] < target[0] else -1 if robot[0] > target[0] else 0
            dy = 1 if robot[1] < target[1] else -1 if robot[1] > target[1] else 0
            if dx != 0 and dy != 0:
                tries = [(dx, 0), (0, dy)]
            else:
                tries = [(dx, dy)]
            # print(f'robot: {robot}, target: {target}, {tries=}')
            for dx, dy in tries:
                new_robot = robot[0] + dx, robot[1] + dy
                if is_gap(pad_for_robot, new_robot):
                    # print(f'GAP {new_robot=}')
                    continue
                # print(f'{robot=} {target=} {dx,dy=} {new_robot=} {DIRECTION[(dx, dy)]=} ')
                new_sequence.add((seq + DIRECTION[(dx, dy)], new_robot))
                # print(f'{new_sequence=}')
        if not new_sequence:
            break
        sequence = new_sequence

    return robot, set([s + 'A' for s in solution])


NUMPAD = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    GAP: (0, 3),
    '0': (1, 3),
    'A': (2, 3),
}
KEYPAD = {
    GAP: (0, 0),
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}


def puzzle1(lines: list[str]):
    robot_at_numpad = (2, 3)
    robot_at_keypad1 = (2, 0)
    robot_at_keypad2 = (2, 0)

    for l in lines:
        sequence_for_line = ''
        for c in l.strip():
            sequence_for_keypad1 = get_sequence_for_sequence(robot_at_numpad, {c}, NUMPAD, KEYPAD)
            sequence_for_keypad1 = get_only_shortest(sequence_for_keypad1)
            print(len(sequence_for_keypad1))
            sequence_for_keypad2 = get_sequence_for_sequence(robot_at_keypad1, sequence_for_keypad1,
                                                             KEYPAD, KEYPAD)
            sequence_for_keypad2 = get_only_shortest(sequence_for_keypad2)
            print(len(sequence_for_keypad2))
            sequence_for_you = get_sequence_for_sequence(robot_at_keypad2, sequence_for_keypad2,
                                                         KEYPAD, KEYPAD)
            sequence_for_you = get_only_shortest(sequence_for_you)
            print(len(sequence_for_you))
            sequence_for_line += sequence_for_you.pop()
        print(sequence_for_line)
    return sequence_for_line


def solve_whole_line(l, robot_at_keypad1, robot_at_keypad2, robot_at_numpad):
    sequence_for_keypad1 = get_sequence_for_sequence(robot_at_numpad, {l.strip()}, NUMPAD, KEYPAD)
    sequence_for_keypad1 = get_only_shortest(sequence_for_keypad1)
    print(len(sequence_for_keypad1))
    sequence_for_keypad2 = get_sequence_for_sequence(robot_at_keypad1, sequence_for_keypad1,
                                                     KEYPAD, KEYPAD)
    sequence_for_keypad2 = get_only_shortest(sequence_for_keypad2)
    print(len(sequence_for_keypad2))
    sequence_for_you = get_sequence_for_sequence(robot_at_keypad2, sequence_for_keypad2,
                                                 KEYPAD, KEYPAD)
    sequence_for_you = get_only_shortest(sequence_for_you)
    print(sequence_for_you)
    return sequence_for_you


def get_only_shortest(seqs: set[str]) -> set[str]:
    shortest = -1
    for s in seqs:
        if len(s) < shortest or shortest == -1:
            shortest = len(s)

    return set([s for s in seqs if len(s) == shortest])


def get_sequence_for_sequence(robot_start: Pos, sequence: set[str], keypad_for_robot: Pad, keypad_to_control: Pad):
    # print(f'{keypad_for_robot=}')
    sequence_for_keypad = {''}
    for s in sequence:
        robot = robot_start
        for c in s:
            # print(c)
            # print(f'{robot=} {keypad_for_robot[c]=}')
            robot, seq_for_keypad = get_sequence_to_push_button(robot, keypad_for_robot[c], keypad_for_robot,
                                                                keypad_to_control)
            new_sequence_for_keypad = set()
            # print(f'{s=} {seq_for_keypad=}')
            for sr in seq_for_keypad:
                new_sequence_for_keypad |= set([ss + sr for ss in sequence_for_keypad])
            sequence_for_keypad = new_sequence_for_keypad
            if len(sequence_for_keypad) == 0:
                print(f'{robot_start=} {sequence=}')
    return sequence_for_keypad


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
