import re


def test_solve():
    puzzle_input = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    assert solve(puzzle_input) == 8


def test_solve2():
    puzzle_input = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    assert solve2(puzzle_input) == 2286


def test_parse():
    game_id, sets = parse("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert game_id == 1
    assert sets == [
        {"blue": 3, "red": 4, "green": 0},
        {"red": 1, "green": 2, "blue": 6},
        {"blue": 0, "red": 0, "green": 2},
    ]


def parse(line):
    m = re.match(r"^Game (\d+): (.*)$", line)
    game_id = int(m.group(1))
    sets = []
    for part in m.group(2).split(";"):
        part = part.strip()
        this_set = {"blue": 0, "green": 0, "red": 0}
        for color in part.split(","):
            color = color.strip()
            m = re.match(r"^(\d+) (\w+)$", color)
            this_set[m.group(2)] = int(m.group(1))
        sets.append(this_set)
    return game_id, sets


def solve(puzzle_input):
    tally = 0
    for l in puzzle_input:
        game_id, sets = parse(l)
        for s in sets:
            if s["blue"] > 14 or s["red"] > 12 or s["green"] > 13:
                break
        else:
            tally += game_id
    return tally


def solve2(puzzle_input):
    tally = 0
    for l in puzzle_input:
        game_id, sets = parse(l)
        mins = {"blue": 0, "green": 0, "red": 0}
        for s in sets:
            for k in mins:
                mins[k] = max(mins[k], s[k])
        tally += mins["blue"] * mins["green"] * mins["red"]
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
