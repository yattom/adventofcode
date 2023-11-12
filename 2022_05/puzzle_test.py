from dataclasses import dataclass
import re

def test_solve():
    puzzle_input = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]",
        " 1   2   3 ",
        "",
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    assert solve(puzzle_input) == "CMZ"


def test_solve2():
    puzzle_input = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]",
        " 1   2   3 ",
        "",
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    assert solve2(puzzle_input) == "MCD"


@dataclass
class Move:
    crates: int
    from_: int
    to: int

    def apply_to(self, stacks: dict[int, list[str]]):
        for i in range(self.crates):
            c = stacks[self.from_].pop()
            stacks[self.to].append(c)


class Move9001(Move):
    def apply_to(self, stacks: dict[int, list[str]]):
        crates = stacks[self.from_][-self.crates:]
        stacks[self.from_] = stacks[self.from_][0:-self.crates]
        stacks[self.to] += crates


def parse(puzzle_input, crane_type=Move):
    lines = iter(puzzle_input)

    init = {}
    while len(l := next(lines)) > 0:
        if l.startswith(" 1"):
            continue
        for i in range(int((len(l) + 1) / 4)):
            c = l[i * 4 + 1]
            if c == " ":
                continue
            assert c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if (i + 1) not in init:
                init[i + 1] = []
            init[i + 1].insert(0, c)

    moves = []
    for l in lines:
        c, f, t = [int(v) for v in re.match(r"move (\d*) from (\d*) to (\d*)", l).groups()]
        moves.append(crane_type(crates=c, from_=f, to=t))

    return init, moves




def test_parse():
    puzzle_input = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]",
        " 1   2   3 ",
        "",
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    init, moves = parse(puzzle_input)
    assert init == {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"]}
    assert moves == [Move(1, 2, 1), Move(3, 1, 3), Move(2, 2, 1), Move(1, 1, 2)]


def solve(puzzle_input):
    init, moves = parse(puzzle_input)
    for m in moves:
        m.apply_to(init)
    
    return "".join([init[i][-1] for i in range(1, len(init) + 1)])


def solve2(puzzle_input):
    init, moves = parse(puzzle_input, crane_type=Move9001)
    for m in moves:
        m.apply_to(init)

    return "".join([init[i][-1] for i in range(1, len(init) + 1)])
    

def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)