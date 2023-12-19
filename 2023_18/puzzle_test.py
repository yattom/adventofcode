def test_solve():
    puzzle_input = [
        "R 6 (#70c710)",
            "D 5 (#0dc571)",
            "L 2 (#5713f0)",
            "D 2 (#d2c081)",
            "R 2 (#59c680)",
            "D 2 (#411b91)",
            "L 5 (#8ceee2)",
            "U 2 (#caa173)",
            "L 1 (#1b58a2)",
            "U 2 (#caa171)",
            "R 2 (#7807d2)",
            "U 3 (#a77fa3)",
            "L 2 (#015232)",
            "U 2 (#7a21e3)",
    ]
    assert solve(puzzle_input) == 62


def test_solve2():
    puzzle_input = [
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
    ]
    assert solve2(puzzle_input) == 952408144115


DIRS = {
    "R": (0, 1),
    "L": (0, -1),
    "D": (1, 0),
    "U": (-1, 0),
}


def solve(puzzle_input):
    plan = generate_plan(puzzle_input, line_parser_1)
    dump(plan)
    print()
    fill(plan)
    dump(plan)
    print()
    return len(plan)


def solve2(puzzle_input):
    plan = generate_plan(puzzle_input, line_parser_2)
    dump(plan, area=((-50, -50), (50, 50)))
    assert False
    fill(plan)
    return len(plan)


def fill(plan: dict[tuple[int, int], str]):
    start = (2, 2)  # assuming the start is always in the inside
    to_fill = {start}
    while to_fill:
        row, col = to_fill.pop()
        if (row, col) in plan:
            continue
        plan[(row, col)] = "#"
        for d in DIRS.values():
            dd = (row + d[0], col + d[1])
            if dd not in plan:
                to_fill.add(dd)


OUTSIDE = 0
INSIDE = 1
ONLINE = 2

def dump(plan: dict[tuple[int, int], str], area=None):
    if area:
        min_row = area[0][0]
        max_row = area[1][0]
        min_col = area[0][1]
        max_col = area[1][1]
    else:
        min_row = min([k[0] for k in plan.keys()])
        max_row = max([k[0] for k in plan.keys()])
        min_col = min([k[1] for k in plan.keys()])
        max_col = max([k[1] for k in plan.keys()])
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if (row, col) in plan:
                print("#", end="")
            else:
                print(".", end="")
        print()


def line_parser_1(line: str) -> tuple[str, int]:
    d, l, _ = line.split()
    return d, int(l)


def line_parser_2(line: str) -> tuple[str, int]:
    print(line)
    _, _, c = line.split()
    l_str = c[2:7]
    l = int(l_str, 16)
    d = ["R", "D", "L", "U"][(int(c[7:8]))]
    return d, l


def generate_plan(puzzle_input: list[str], parser) -> dict[tuple[int, int], str]:
    plan: dict[tuple[int, int], str] = {}
    row = col = 1
    for line in puzzle_input:
        d, l = parser(line)
        plan[(row, col)] = "#"
        for i in range(l):
            plan[(row, col)] = "#"
            row += DIRS[d][0]
            col += DIRS[d][1]
        plan[(row, col)] = "#"
    return plan


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)