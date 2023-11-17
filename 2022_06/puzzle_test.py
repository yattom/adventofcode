def test_solve():
    assert solve(["mjqjpqmgbljsphdztnvjfqwrcgsmlb"]) == 7


def is_unique(s, end_idx, length):
    for i in range(end_idx - length + 1, end_idx + 1):
        for j in range(i + 1, end_idx + 1):
            if s[i] == s[j]:
                return False
    return True


def solve(puzzle_input):
    l = puzzle_input[0]
    for i in range(4, len(l)):
        if is_unique(l, i, 4):
            return i + 1
    return -1


def solve2(puzzle_input):
    l = puzzle_input[0]
    for i in range(14, len(l)):
        if is_unique(l, i, 14):
            return i + 1
    return -1


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)