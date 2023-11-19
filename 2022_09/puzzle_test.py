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



def solve(puzzle_input):
    head = tail = (0, 0)
    visited = set([tail])
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
            head = add(head, vector)
            if distance(head, tail) > 1:
                tail = (tail[0] + sign(head[0] - tail[0]), tail[1] + sign(head[1] - tail[1]))
            visited.add(tail)
    return len(visited)


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