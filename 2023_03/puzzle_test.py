import re


def test_solve():
    puzzle_input = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    assert solve(puzzle_input) == 4361

def test_solve2():
    puzzle_input = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    assert solve2(puzzle_input) == 467835


def solve(puzzle_input):
    numbers = []
    symbols = {}
    for y, l in enumerate(puzzle_input):
        x = 0
        while x < len(l):
            if l[x] in '0123456789':
                n = re.match(r"(\d+).*", l[x:]).group(1)
                numbers.append((int(n), x, y, len(n)))
                x += len(n) - 1
            elif l[x] != '.':
                symbols[(x, y)] = l[x]
            x += 1

    tally = 0
    def is_part_no(x, y, l):
        for xx in range(x - 1, x + l + 1):
            for yy in range(y - 1, y + 2):
                if (xx, yy) in symbols:
                    return True
        return False

    for n, x, y, l in numbers:
        if is_part_no(x, y, l):
            tally += n
    return tally


def solve2(puzzle_input):
    numbers = []
    symbols = {}
    for y, l in enumerate(puzzle_input):
        x = 0
        while x < len(l):
            if l[x] in '0123456789':
                n = re.match(r"(\d+).*", l[x:]).group(1)
                numbers.append((int(n), x, y, len(n)))
                x += len(n) - 1
            elif l[x] != '.':
                symbols[(x, y)] = l[x]
            x += 1

    tally = 0
    for loc, symbol in symbols.items():
        if symbol != '*':
            continue
        gear_x, gear_y = loc
        gear_numbers = []
        for n, x, y, l in numbers:
            if x - 1 <= gear_x <= x + l and y - 1 <= gear_y <= y + 1:
                gear_numbers.append(n)
        if len(gear_numbers) != 2:
            continue
        print(gear_numbers)
        tally += gear_numbers[0] * gear_numbers[1]
    return tally


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
