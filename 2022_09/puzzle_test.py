def test_solve():
    puzzle_input = [
        "R 4",
        "U 4",
        "L 3",
        "D 1",
        "R 4",
        "D 1",
        "L 5",
        "R 2",
    ]
    assert solve(puzzle_input) == 13


def test_solve2():
    puzzle_input = [
        "R 4",
        "U 4",
        "L 3",
        "D 1",
        "R 4",
        "D 1",
        "L 5",
        "R 2",
    ]
    assert solve2(puzzle_input) == 1


def test_solve2_2():
    puzzle_input = [
        "R 5",
        "U 8",
        "L 8",
        "D 3",
        "R 17",
        "D 10",
        "L 25",
        "U 20",
    ]
    assert solve2(puzzle_input) == 36


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0


def solve(puzzle_input, knots=2):
    tails = [(0, 0)] * knots
    visited = {tails[-1]}
    for direction, steps in [l.split(" ") for l in puzzle_input]:
        match direction:
            case "R":
                vector = (1, 0)
            case "L":
                vector = (-1, 0)
            case "D":
                vector = (0, 1)
            case "U":
                vector = (0, -1)
            case _:
                raise ValueError(f"{direction=}, {steps=}")
        for i in range(int(steps)):
            tails[0] = add(tails[0], vector)
            for j in range(1, len(tails)):
                if distance(tails[j - 1], tails[j]) > 1:
                    tails[j] = (tails[j][0] + sign(tails[j - 1][0] - tails[j][0]), tails[j][1] + sign(tails[j - 1][1] - tails[j][1]))
            visited.add(tails[-1])
    return len(visited)


def solve2(puzzle_input):
    return solve(puzzle_input, 10)


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)