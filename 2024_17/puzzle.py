import time


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


def combo_operand(registers: dict[str, int], operand: int) -> int:
    match operand:
        case _ if operand <= 3:
            return operand
        case 4:
            return registers['A']
        case 5:
            return registers['B']
        case 6:
            return registers['C']
        case 7:
            raise ValueError('Invalid operand')
        case _:
            raise ValueError('Invalid operand')


def puzzle1(lines: list[str]):
    code, registers = parse_program(lines)

    out = run_code(code, registers)

    return ','.join([str(v) for v in out])


def parse_program(lines):
    registers = {}
    for l in lines:
        if l.startswith('Register'):
            reg = l[9]
            val = int(l[12:])
            registers[reg] = val
        if l.startswith('Program'):
            code = [int(v) for v in l.strip()[9:].split(',')]
    return code, registers


def run_code(code, registers):
    ip = 0
    out = []
    while 0 <= ip < len(code):
        inst = code[ip]
        operand = code[ip + 1]
        # print(f'{ip=}, {inst=}, {operand=}, {registers=}')

        match inst:
            case 0:
                # adv
                registers['A'] = registers['A'] // (2 ** combo_operand(registers, operand))
                ip += 2
            case 1:
                # bxl
                registers['B'] = operand ^ registers['B']
                ip += 2
            case 2:
                # bst
                registers['B'] = combo_operand(registers, operand) % 8
                ip += 2
            case 3:
                # jnz
                if registers['A'] != 0:
                    ip = operand
                else:
                    ip += 2
            case 4:
                # bxc
                registers['B'] = registers['B'] ^ registers['C']
                ip += 2
            case 5:
                # out
                out.append(combo_operand(registers, operand) % 8)
                ip += 2
            case 6:
                # bdv
                registers['B'] = registers['A'] // (2 ** combo_operand(registers, operand))
                ip += 2
            case 7:
                # cdv
                registers['C'] = registers['A'] // (2 ** combo_operand(registers, operand))
                ip += 2
            case _:
                raise ValueError('Invalid instruction')
    return out



def puzzle2(lines: list[str]):
    code, registers = parse_program(lines)
    print(f'{code=}')
    def trial(i):
        registers['A'] = i
        return run_code(code, registers)
    i = 10
    min_i = max_i = None
    while not min_i or not max_i:
        out = trial(i)
        if len(out) < len(code):
            min_i = i
        if len(code) < len(out):
            max_i = i
        i = int(i * 1.1)
    print(f'{min_i=}, {max_i=}')

    def search(digit: int, min_i: int, max_i: int, split=1024) -> int:
        while True:
            next_min_i = next_max_i = None
            if max_i - min_i < 1000 * 1000:
                step = 1
            else:
                step = (max_i - min_i) // split
            print(f'{min_i=}, {max_i=}, {step=}')
            for i in range(min_i, max_i, step):
                out = trial(i)
                if out == code:
                    return i
                if out[digit:] == code[digit:]:
                    if not next_min_i:
                        next_min_i = i - step
                if out[digit:] != code[digit:] and next_min_i:
                    if not next_max_i:
                        next_max_i = i
                print(f'{digit=} {i=:,d}, {out=} {next_min_i=}, {next_max_i=}')
                if next_min_i and next_max_i:
                    v = search(digit - 1, next_min_i, next_max_i)
                    if v >= 0:
                        return v
                    next_min_i =  next_max_i = None
            else:
                return -1

    answer = search(- 1, min_i, max_i)
    print(f'{answer=:,d} {code=} {trial(answer)=}')
    return answer


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
