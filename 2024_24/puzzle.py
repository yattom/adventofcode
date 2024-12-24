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


dp = DebugPrinter(enabled=True, interval=10 * 1000 * 1000 * 1000)

Label: TypeAlias = str


@dataclass()
class Gate:
    logic: str
    ins: list[Label]
    out: Label


def get_gate_for_ins(gates: list[Gate], label: str) -> list[Gate]:
    result = []
    for gate in gates:
        if label in gate.ins:
            result.append(gate)
    return result


def get_gate_for_out(gates: list[Gate], label: str) -> Gate:
    result = []
    for gate in gates:
        if label == gate.out:
            return gate


def puzzle1(lines: list[str]):
    gates, input_values = read_input(lines)

    values = resolve_output(gates, input_values)
    print(f'{len(values)=}')

    z_labels = sorted([l for l in values if l.startswith('z')], reverse=True)
    value = calc_value(values, z_labels)
    return value


def calc_value(values, labels):
    label_values = [values[l] for l in labels]
    # print(f'{label_values=}')
    value = 0
    for i, v in enumerate(label_values):
        value = value * 2 + v
    return value


def calc_bits(values, labels):
    label_values = [(values[l] if l in values else 0) for l in labels]
    bits = ''
    for i, v in enumerate(label_values):
        bits += str(v)
    return bits.strip()


def format_bits(bits):
    result = ''
    for i in range(0, len(bits)):
        result += bits[i]
        if i % 16 == 15:
            result += ':'
        elif i % 4 == 3:
            result += ' '
    return result.strip()


def resolve_output(gates: list[Gate], input_values: dict[Label, int]):
    no_value = -1
    values = input_values.copy()
    changed = True
    while changed:
        # print(f'{values=}')
        changed = False
        for gate in gates:
            if gate.out in values:
                continue
            in1 = values.get(gate.ins[0], no_value)
            in2 = values.get(gate.ins[1], no_value)
            if in1 == no_value or in2 == no_value:
                continue
            match gate.logic:
                case 'AND':
                    values[gate.out] = in1 & in2
                case 'OR':
                    values[gate.out] = in1 | in2
                case 'XOR':
                    values[gate.out] = in1 ^ in2
                case _:
                    raise RuntimeError(f'Unknown logic: {gate.logic}')
            changed = True
    return values


def read_input(lines):
    input_values = dict()
    for i, l in enumerate(lines):
        if l.strip() == '':
            break
        label, value = (v.strip() for v in l.split(':'))
        input_values[label] = int(value)
    gates = []
    for l in lines[i + 1:]:
        in1, logic, in2, _, out = l.strip().split(' ')
        gates.append(Gate(logic, [in1, in2], out))
    return gates, input_values


def combination(length: int, min_and_max: tuple[int, int]):
    value = [i for i in range(min_and_max[0], length)]
    print(f'{value=}')
    while True:
        yield value[:]
        for i in range(len(value) - 1, -1, -1):
            if value[i] + 1 > min_and_max[1]:
                if i == 0:
                    return
                value[i] = min_and_max[0]
            else:
                value[i] += 1
                break


def set_x_y_values(values, x_labels, y_labels, x, y):
    bin_x = bin(x)[2:]
    bin_y = bin(y)[2:]

    for xl in x_labels:
        i = int(xl[1:])
        if i >= len(bin_x):
            values[xl] = 0
        else:
            values[xl] = int(bin_x[-i])
    for yl in y_labels:
        i = int(yl[1:])
        if i >= len(bin_y):
            values[yl] = 0
        else:
            values[yl] = int(bin_y[-i])


def get_different_z_labels(actual_z_bits, expected_z_bits):
    result = []
    for i in range(len(expected_z_bits) - 1, -1, -1):
        if expected_z_bits[i] != actual_z_bits[i]:
            result.append(f'z{i:02}')
    return result


def find_suspicious_gates(gates: list[Gate], different_z_labels: list[str], suspicious_gates: set[str]) -> set[
    Label]:
    found: set[Label] = set()
    gates_to_check: set[str] = set(different_z_labels)
    while gates_to_check:
        if len(found) > 8:
            return found
        gate: Gate = get_gate_for_out(gates, gates_to_check.pop())
        if gate.out in found:
            continue
        for input_label in gate.ins:
            in_gates = get_gate_for_ins(gates, input_label)
            for g in in_gates:
                if g.out in suspicious_gates:
                    gates_to_check.add(g.out)
                else:
                    found.add(g.out)
    else:
        print('No suspicious gates found')
    return found


def puzzle2(lines: list[str]):
    puzzle = read_input(lines)
    gates: list[Gate] = puzzle[0]
    input_values: dict[Label, int] = puzzle[1]

    # calculate expected
    x_labels = sorted([l for l in input_values if l.startswith('x')], reverse=True)
    y_labels = sorted([l for l in input_values if l.startswith('y')], reverse=True)
    resolved = resolve_output(gates, input_values)
    z_labels = sorted([l for l in resolved if l.startswith('z')], reverse=True)
    expected_z_value = calc_value(input_values, x_labels) + calc_value(input_values, y_labels)
    expected_z_bits = bin(expected_z_value)[2:]

    x = y = 0
    suspicious_gates: set[Label] = set()
    while True:
        values = input_values.copy()
        set_x_y_values(values, x_labels, y_labels, x, y)
        resolved = resolve_output(gates, values)
        actual_z_bits = calc_bits(resolved, z_labels)
        if actual_z_bits == expected_z_bits:
            break
        different_z_labels = get_different_z_labels(actual_z_bits, expected_z_bits)
        suspicious_gates |= find_suspicious_gates(gates, different_z_labels, suspicious_gates)

        if len(suspicious_gates) >= 8:
            labels = try_swapping(gates, input_values, suspicious_gates)
            if labels:
                # nailed it!
                break

        x = x << 1 | ~(x & 1)
        y = y >> 1 | (2 ** 44)

    print(f'{labels=} {z_labels=} {actual_z_bits=} {expected_z_value=}')
    for i in range(0, len(labels), 2):
        if labels[i] > labels[i + 1]:
            labels[i], labels[i + 1] = labels[i + 1], labels[i]

    print(','.join(labels))
    return ','.join(labels)


def try_swapping(gates: list[Gate], input_values: dict[Label, int], suspicious_gates: set[Label]) -> list[Label] | None:
    print(f'try swapping {suspicious_gates=}')
    SWAP_PAIRS = 4
    x_labels = sorted([l for l in input_values if l.startswith('x')], reverse=True)
    y_labels = sorted([l for l in input_values if l.startswith('y')], reverse=True)
    resolved = resolve_output(gates, input_values)
    z_labels = sorted([l for l in resolved if l.startswith('z')], reverse=True)
    expected_z_value = calc_value(input_values, x_labels) + calc_value(input_values, y_labels)
    expected_z_bits = bin(expected_z_value)[2:]

    # TODO in process of modifying
    for c in combination(SWAP_PAIRS * 2, (0, len(suspicious_gates) - 1)):
        if len(c) != len(set(c)):
            # no swapping same gate
            continue
        for i in range(SWAP_PAIRS):
            gates[c[i * 2]].out, gates[c[i * 2 + 1]].out = gates[c[i * 2 + 1]].out, gates[c[i * 2]].out
        resolved = resolve_output(gates, input_values)
        actual_z_bits = calc_bits(resolved, z_labels)

        if dp.at_interval():
            print(f'{c=}')
            print(f'{suspicious_gates=}')
            print(f'  {actual_z_bits=}')
            print(f'{expected_z_bits=}')
        # swap back
        for i in range(SWAP_PAIRS):
            gates[c[i * 2]].out, gates[c[i * 2 + 1]].out = gates[c[i * 2 + 1]].out, gates[c[i * 2]].out

        if actual_z_bits == expected_z_bits:
            return [gates[i].out for i in c]

    return None


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
