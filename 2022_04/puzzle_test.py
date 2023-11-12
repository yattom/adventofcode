def test_solve():
    puzzle_input = [
        "2-4,6-8",
        "2-3,4-5",
        "5-7,7-9",
        "2-8,3-7",
        "6-6,4-6",
        "2-6,4-8",        
    ]
    assert solve(puzzle_input) == 2


def test_solve2():
    puzzle_input = [
        "2-4,6-8",
        "2-3,4-5",
        "5-7,7-9",
        "2-8,3-7",
        "6-6,4-6",
        "2-6,4-8",        
    ]
    assert solve2(puzzle_input) == 4


def solve(puzzle_input):
    contained = 0
    for l in puzzle_input:
        p1, p2 = l.split(",")
        p1_s, p1_e = [int(v) for v in p1.split("-")]
        p2_s, p2_e = [int(v) for v in p2.split("-")]
        if p1_s >= p2_s and p1_e <= p2_e:
            contained += 1
        elif p2_s >= p1_s and p2_e <= p1_e:
            contained += 1
    return contained


def solve2(puzzle_input):
    contained = 0
    for l in puzzle_input:
        p1, p2 = l.split(",")
        p1_s, p1_e = [int(v) for v in p1.split("-")]
        p2_s, p2_e = [int(v) for v in p2.split("-")]
        if (p1_s <= p2_s and p2_s <= p1_e) or (p2_s <= p1_s and p1_s <= p2_e):
            contained += 1
    return contained


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)