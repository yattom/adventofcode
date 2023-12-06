import re


def test_solve():
    puzzle_input = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]
    assert solve(puzzle_input) == 13


def test_solve2():
    puzzle_input = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]
    assert solve2(puzzle_input) == 30


def solve(puzzle_input):
    tally = 0
    wins = [False] * 100
    for l in puzzle_input:
        m = re.match(r"Card +(\d+): ([ \d]*) \| (.*)", l)
        card_id, winning, yours = m.groups()
        for i in range(len(wins)):
            wins[i] = False
        for w in winning.split():
            wins[int(w)] = True
        score = 0
        for y in yours.split():
            if wins[int(y)]:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        tally += score
    return tally


def solve2(puzzle_input):
    copies = [1] * len(puzzle_input)
    wins = [False] * 100
    for l in puzzle_input:
        m = re.match(r"Card +(\d+): ([ \d]*) \| (.*)", l)
        card_id, winning, yours = m.groups()
        for i in range(len(wins)):
            wins[i] = False
        for w in winning.split():
            wins[int(w)] = True
        hit = 0
        for y in yours.split():
            if wins[int(y)]:
                hit += 1
        for i in range(int(card_id), int(card_id) + hit):
            if i > len(puzzle_input) - 1:
                break
            copies[i] += copies[int(card_id) - 1]
        print(copies)
    return sum(copies)



def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
