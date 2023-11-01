import pytest

WIN = "win"
LOSE = "lose"
DRAW = "draw"
RPS_TABLE = {
    ('A', 'X'): DRAW,
    ('A', 'Y'): WIN,
    ('A', 'Z'): LOSE,
    ('B', 'X'): LOSE,
    ('B', 'Y'): DRAW,
    ('B', 'Z'): WIN,
    ('C', 'X'): WIN,
    ('C', 'Y'): LOSE,
    ('C', 'Z'): DRAW,
}

SCORE_TABLE = {
    WIN: 6,
    DRAW: 3,
    LOSE: 0,
    'X': 1,
    'Y': 2,
    'Z': 3,
}


def game(elf, you):
    return RPS_TABLE[(elf, you)]


def calc_you(elf, result):
    for (e, you), r in RPS_TABLE.items():
        if e == elf and r == result:
            return you


def score(elf, you):
    return SCORE_TABLE[you] + SCORE_TABLE[game(elf, you)]


@pytest.mark.parametrize(
    "elf,you,result",
    [
        ('A', 'Y', WIN),
        ('A', 'Z', LOSE),
        ('B', 'Y', DRAW),
    ]
)
def test_winning(elf, you, result):
    assert game(elf, you) == result


def test_scoring():
    assert score('A', 'Y') == 8


def test_calc_you():
    assert calc_you('A', WIN) == 'Y'
    assert calc_you('A', LOSE) == 'Z'
    assert calc_you('A', DRAW) == 'X'
    assert calc_you('B', WIN) == 'Z'
    assert calc_you('B', LOSE) == 'X'
    assert calc_you('B', DRAW) == 'Y'


def 問題1(puzzle_input: list[str]):
    total = 0
    for l in puzzle_input:
        elf, you = l.split()
        total += score(elf, you)
    print(total)


def 問題2(puzzle_input: list[str]):
    RESULTS = {
        'X': LOSE,
        'Y': DRAW,
        'Z': WIN,
    }
    total = 0
    for l in puzzle_input:
        elf, result = l.split()
        you = calc_you(elf, RESULTS[result])
        total += score(elf, you)
    print(total)


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
