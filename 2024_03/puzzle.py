import re

def puzzle1(lines: list[str]):
    line = ''.join(lines)
    total = 0
    muls = re.findall(r'mul\(\d+,\d+\)', line)
    for inst in muls:
        a, b = re.match(r'mul\((\d+),(\d+)\)', inst).groups()
        total += int(a) * int(b)
    return total


def puzzle2(lines: list[str]):
    line = ''.join(lines)
    total = 0
    enabled = True
    instructions = re.findall(r"do\(\)|mul\(\d+,\d+\)|don't\(\)", line)
    for inst in instructions:
        if inst == 'do()':
            enabled = True
        elif inst == "don't()":
            enabled = False
        else:
            if enabled:
                a, b = re.match(r'mul\((\d+),(\d+)\)', inst).groups()
                total += int(a) * int(b)
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
