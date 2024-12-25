import random
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


gate_ins_map: dict[Label, list[Gate]] = {}


def get_gate_for_ins(gates: dict[Label, Gate], label: str) -> list[Gate]:
    if label in gate_ins_map:
        return gate_ins_map[label][:]
    result = []
    for gate in gates.values():
        if label in gate.ins:
            result.append(gate)
    gate_ins_map[label] = result
    return result


def get_gate_for_out(gates: dict[Label, Gate], label: str) -> Gate:
    result = []
    for gate in gates.values():
        if label == gate.out:
            return gate


def puzzle1(lines: list[str]):
    gates, input_values = read_input(lines)

    values = resolve_output(gates, input_values)
    # print(f'puzzle1 {len(values)=} {values=}')

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


def resolve_output(gates: dict[Label, Gate], input_values: dict[Label, int]):
    no_value = -1
    gate_label_to_resolve = list(input_values.keys())
    values = input_values.copy()
    while gate_label_to_resolve:
        changed = False
        new_label_to_resolve = []
        for label in gate_label_to_resolve:
            invoked_gates = get_gate_for_ins(gates, label)
            for gate in invoked_gates:
                if gate.out in values:
                    # already resolved
                    continue
                in1 = values.get(gate.ins[0], no_value)
                in2 = values.get(gate.ins[1], no_value)
                if in1 == no_value or in2 == no_value:
                    # not both input are ready
                    new_label_to_resolve.append(gate.out)
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

                new_label_to_resolve.append(gate.out)
                changed = True
        if not changed:
            break
        gate_label_to_resolve += new_label_to_resolve
    return values


def read_input(lines):
    '''
    
    :param lines: List of input strings containing gate and input value definitions.
    :return: A tuple with two elements:
             - A dictionary where keys are gate labels for output (str) and values are Gate objects.
             - A dictionary where keys are input labels (str) and values are their corresponding integer values.
    '''
    input_values = dict()
    for i, l in enumerate(lines):
        if l.strip() == '':
            break
        label, value = (v.strip() for v in l.split(':'))
        input_values[label] = int(value)
    gates: dict[Label, Gate] = {}
    for l in lines[i + 1:]:
        in1, logic, in2, _, out = l.strip().split(' ')
        gates[out] = Gate(logic, [in1, in2], out)
    return gates, input_values


@dataclass
class Puzzle:
    gates: dict[Label, Gate]
    input_values: dict[Label, int]
    labels: set[Label]
    x_labels: list[Label]
    y_labels: list[Label]
    z_labels: list[Label]

    @staticmethod
    def build_puzzle(lines) -> 'Puzzle':
        read_data = read_input(lines)
        gates: dict[Label, Gate] = read_data[0]
        input_values: dict[Label, int] = read_data[1]
        labels: set[Label] = set(gates.keys()) | set(input_values.keys())

        x_labels = sorted([l for l in labels if l.startswith('x')], reverse=True)
        y_labels = sorted([l for l in labels if l.startswith('y')], reverse=True)
        z_labels = sorted([l for l in labels if l.startswith('z')], reverse=True)

        puzzle = Puzzle(gates, input_values, labels, x_labels, y_labels, z_labels)
        return puzzle


Solution: TypeAlias = tuple[tuple[Label, Label]]


@dataclass
class Working:
    suspicious_gates: dict[Label, int] = field(default_factory=dict)
    failed_gates: set[Solution] = field(default_factory=set)
    solved: bool = False


# def all_combination_of_pairs(number_of_pairs: int, min_and_max: tuple[int, int]):
#     value = [i for i in range(min_and_max[0], number_of_pairs)]
#     print(f'{value=}')
#     while True:
#         yield value[:]
#         for i in range(len(value) - 1, -1, -1):
#             if value[i] + 1 > min_and_max[1]:
#                 if i == 0:
#                     return
#                 value[i] = min_and_max[0]
#             else:
#                 value[i] += 1
#                 break
def all_combination_of_pairs(number_of_pairs: int, min_and_max: tuple[int, int]):
    # Step 1: 数字のリストを生成
    numbers = list(range(min_and_max[0], min_and_max[1] + 1))
    total_numbers = len(numbers)

    # ガード: 入力データがペアを作るのに十分でない場合は終了
    if number_of_pairs * 2 > total_numbers:
        return

    # Step 2: 各ペアのインデックスリストを生成
    indices = list(range(2 * number_of_pairs))  # インデックスの最初のセット
    while True:
        # 現在のインデックスを使ってペアを生成
        result = []
        for i in range(0, len(indices), 2):
            result.append((numbers[indices[i]], numbers[indices[i + 1]]))

        yield result

        # 次のインデックスセットを生成
        for i in range(len(indices) - 1, -1, -1):
            if indices[i] != total_numbers - len(indices) + i:
                break
        else:
            return  # インデックスが限界に達した場合は終了

        indices[i] += 1
        for j in range(i + 1, len(indices)):
            indices[j] = indices[j - 1] + 1


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


def find_suspicious_gates(puzzle: Puzzle, different_z_labels: list[str], working: Working):
    gates_to_check: set[str] = set(different_z_labels)
    while gates_to_check:
        gate: Gate = get_gate_for_out(puzzle.gates, gates_to_check.pop())
        for input_label in gate.ins:
            in_gate = get_gate_for_out(puzzle.gates, input_label)
            if not in_gate:
                # system input; just ignore
                continue
            if in_gate.out not in working.suspicious_gates:
                working.suspicious_gates[in_gate.out] = 0
            working.suspicious_gates[in_gate.out] += 1
    else:
        # print('No suspicious gates found')
        pass


def generate_testing_values_bit_by_bit(puzzle: Puzzle, working: Working):
    for bit in range(len(puzzle.x_labels)):
        for xval, yval in [(0, 1), (1, 0), (1, 1)]:
            x = xval << bit
            y = yval << bit
            yield x, y


def generate_testing_values_bit_by_bit_thorough(puzzle: Puzzle, working: Working):
    for x_bit in range(len(puzzle.x_labels)):
        for y_bit in range(len(puzzle.x_labels)):
            for xval, yval in [(0, 1), (1, 0), (1, 1)]:
                x = xval << x_bit
                y = yval << y_bit
                yield x, y


def generate_testing_values_by_random(puzzle: Puzzle, working: Working):
    min_val = 0
    max_val = 2 ** len(puzzle.x_labels) - 1
    for i in range(10000):
        x = random.randint(min_val, max_val)
        y = random.randint(min_val, max_val)
        yield x, y


def gather_suspicious_gates(puzzle, working, strategy):
    for x, y in strategy(puzzle, working):
        z = x + y
        expected_z_bits = bin(z)[2:]

        values = puzzle.input_values.copy()
        set_x_y_values(values, puzzle.x_labels, puzzle.y_labels, x, y)
        resolved = resolve_output(puzzle.gates, values)
        actual_z_bits = calc_bits(resolved, puzzle.z_labels)
        different_z_labels = get_different_z_labels(actual_z_bits, expected_z_bits)
        for z_label in different_z_labels:
            if z_label not in working.suspicious_gates:
                working.suspicious_gates[z_label] = 0
            working.suspicious_gates[z_label] += 1
        find_suspicious_gates(puzzle, different_z_labels, working)


def puzzle2(lines: list[str]):
    puzzle = Puzzle.build_puzzle(lines)

    working = Working()
    gather_suspicious_gates(puzzle, working, generate_testing_values_by_random)
    print(f'{sorted(working.suspicious_gates.items(), key=lambda x: -x[1])=}')

    print(len(working.suspicious_gates))
    return 0

    for i in range(0, len(answer_labels), 2):
        if answer_labels[i] > answer_labels[i + 1]:
            answer_labels[i], answer_labels[i + 1] = answer_labels[i + 1], answer_labels[i]

    print(','.join(answer_labels))
    return ','.join(answer_labels)


def try_swapping(gates: dict[Label, Gate], input_values: dict[Label, int], suspicious_gates: set[Label]) -> list[
                                                                                                                Label] | None:
    gate_labels = list(gates.keys())
    print(f'try swapping {suspicious_gates=}')
    SWAP_PAIRS = 4
    x_labels = sorted([l for l in input_values if l.startswith('x')], reverse=True)
    y_labels = sorted([l for l in input_values if l.startswith('y')], reverse=True)
    resolved = resolve_output(gates, input_values)
    z_labels = sorted([l for l in resolved if l.startswith('z')], reverse=True)
    expected_z_value = calc_value(input_values, x_labels) + calc_value(input_values, y_labels)
    expected_z_bits = bin(expected_z_value)[2:]

    # TODO in process of modifying
    for c in all_combination_of_pairs(SWAP_PAIRS * 2, (0, len(suspicious_gates) - 1)):
        print(c)
        if len(c) != len(set(c)):
            # no swapping same gate
            continue
        for i in range(SWAP_PAIRS):
            label1, label2 = gate_labels[c[i * 2]], gate_labels[c[i * 2 + 1]]
            gates[label1].out, gates[label2].out = gates[label2].out, gates[label1].out
        resolved = resolve_output(gates, input_values)
        actual_z_bits = calc_bits(resolved, z_labels)

        if dp.at_interval():
            print(f'{c=}')
            print(f'{suspicious_gates=}')
            print(f'  {actual_z_bits=}')
            print(f'{expected_z_bits=}')
            import sys
            sys.exit(0)
        # swap back
        for i in range(SWAP_PAIRS):
            label1, label2 = gate_labels[c[i * 2]], gate_labels[c[i * 2 + 1]]
            gates[label1].out, gates[label2].out = gates[label2].out, gates[label1].out

        if actual_z_bits == expected_z_bits:
            return [gates[gates.keys()[i]].out for i in c]

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
