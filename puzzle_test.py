def test_solve():
    puzzle_input = [

    ]
    assert solve(puzzle_input) == 0


def solve(puzzle_input):
    pass


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