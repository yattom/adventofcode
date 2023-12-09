def test_solve():
    puzzle_input = [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45",
    ]
    assert solve(puzzle_input) == 114


def test_solve2():
    puzzle_input = [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45",
    ]
    assert solve2(puzzle_input) == 2


def calc_next_value(values):
    backtracks = [values]
    while True:
        diffs = [values[i + 1] - values[i] for i in range(len(values) - 1)]
        backtracks.append(diffs)
        if all([v == 0 for v in diffs]):
            break
        values = diffs

    print(backtracks)
    last_value = 0
    prev_value = 0
    for values in backtracks[::-1]:
        last_value += values[-1]
        prev_value = values[0] - prev_value
    return prev_value, last_value


def solve(puzzle_input):
    tally = 0
    for l in puzzle_input:
        _, last_value = calc_next_value([int(v) for v in l.split()])
        tally += last_value
    return tally



def solve2(puzzle_input):
    tally = 0
    for l in puzzle_input:
        prev_value, _ = calc_next_value([int(v) for v in l.split()])
        tally += prev_value
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