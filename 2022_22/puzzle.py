from typing import Tuple
import re


class Board:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.height = len(lines)
        self.width = max([len(l) for l in lines])

    def is_floor(self, loc: Tuple[int, int]):
        return self.get(loc) == "."

    def get(self, loc: tuple[int, int]):
        row, col = loc
        if row <= 0 or col <= 0 or row > self.height or col > len(self.lines[row - 1]):
            return " "
        return self.lines[row - 1][col - 1]

    def is_wall(self, loc):
        return self.get(loc) == "#"

    def is_off(self, loc):
        return self.get(loc) == " "


def add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


class Counter:
    FACING = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, board):
        self.board = board
        self.facing = Counter.FACING[0]
        for col in range(1, board.width + 1):
            if board.is_floor((1, col)):
                self.loc = (1, col)
                break

    def forward(self, steps: int):
        for i in range(steps):
            new_loc = add(self.loc, self.facing)
            if self.board.is_off(new_loc):
                new_loc = self.warp()
            if self.board.is_wall(new_loc):
                break
            self.loc = new_loc

    def warp(self):
        new_loc = self.loc
        while not self.board.is_off(new_loc):
            new_loc = sub(new_loc, self.facing)
        return add(new_loc, self.facing)

    def turn(self, direction):
        match direction:
            case "R":
                self.facing = Counter.FACING[(Counter.FACING.index(self.facing) + 1) % 4]
            case "L":
                self.facing = Counter.FACING[(Counter.FACING.index(self.facing) - 1) % 4]


def parse(puzzle_input: list[str]):
    board = Board(puzzle_input[0:puzzle_input.index("")])
    inst_line = puzzle_input.index("")

    # split inst_line into (int, "R" or "L", int, "R" or "L", ...)
    instructions = [(s if s in "RL" else int(s))
                    for s in re.findall(r"\d+|[RL]", puzzle_input[inst_line + 1])]

    return board, instructions


class Cube:
    def __init__(self, lines):
        self.lines = lines
        self.height = len(lines)
        self.width = max([len(l) for l in lines])

    @staticmethod
    def topmost_length(lines: list[str]):
        re.match(" *([^ ]+) ")


def score(counter: Counter):
    return counter.loc[0] * 1000 + counter.loc[1] * 4 + Counter.FACING.index(counter.facing)


def solve(puzzle_input: list[str]):
    board, instructions = parse(puzzle_input)
    counter = Counter(board)
    for inst in instructions:
        if type(inst) is int:
            counter.forward(inst)
        else:
            counter.turn(inst)
    return score(counter)


def solve2(puzzle_input):
    pass


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
