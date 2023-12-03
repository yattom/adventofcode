from dataclasses import dataclass
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


@dataclass(unsafe_hash=True, frozen=True)
class Rect:
    left: int
    top: int
    width: int
    height: int

    @property
    def right(self):
        return self.left + self.width - 1

    @property
    def bottom(self):
        return self.top + self.height - 1

    def is_over_wrap(self, other):
        return not (self.right < other.left or other.right < self.left or
                    self.bottom < other.top or other.bottom < self.top)

    def margin(self, width):
        return Rect(self.left - width, self.top - width,
                    self.width + width * 2, self.height + width * 2)

    def is_inside(self, loc):
        return self.left <= loc[0] <= self.right and self.top <= loc[1] <= self.bottom


def parse(puzzle_input):
    numbers = []
    symbols = {}
    for y, l in enumerate(puzzle_input):
        x = 0
        while x < len(l):
            if l[x] in '0123456789':
                n = re.match(r"(\d+).*", l[x:]).group(1)
                numbers.append((int(n), Rect(x, y, len(n), 1)))
                x += len(n) - 1
            elif l[x] != '.':
                symbols[Rect(x, y, 1, 1)] = l[x]
            x += 1
    return numbers, symbols


def solve(puzzle_input):
    numbers, symbols = parse(puzzle_input)

    def is_part_no(rect):
        for sr in symbols.keys():
            if rect.is_over_wrap(sr):
                return True
        return False

    tally = sum([n for n, r in numbers if is_part_no(r.margin(1))])
    return tally


def solve2(puzzle_input):
    numbers, symbols = parse(puzzle_input)

    tally = 0
    for gear_rect, symbol in symbols.items():
        if symbol != '*':
            continue
        gear_margin = gear_rect.margin(1)
        gear_numbers = [n for n, r in numbers if gear_margin.is_over_wrap(r)]
        if len(gear_numbers) != 2:
            continue
        # print(gear_numbers)
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
