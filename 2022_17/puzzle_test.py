from dataclasses import dataclass


ROCK_PATTERNS = [
    [
        "####",
    ],
    [
        ".#.",
        "###",
        ".#.",
    ],
    [
        "..#",
        "..#",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]


def build_rocks(rock_patterns):
    '''
    ROCK_PATTERNSに現れる形から'#'の座標(x,y)を取り出し、setに格納する

    :param ROCK_PATTERNS:
    :return:
    '''
    rocks = []
    for pat in rock_patterns:
        pos = set()
        for y, line in enumerate(pat):
            for x, c in enumerate(line):
                if c == '#':
                    pos.add((x, -y))
        rocks.append(pos)
    return rocks


def test_build_rocks():
    rocks = build_rocks(ROCK_PATTERNS)
    assert 5 == len(rocks)
    assert {(0, 0), (1, 0), (2, 0), (3, 0)} == rocks[0]
    assert {(1, -2), (0, -1), (1, -1), (2, -1), (1, 0)} == rocks[1]


class Cave:
    WIDTH = 7
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self):
        self.filled = set()
        self.top_rock = 0

    def is_empty(self, x, y):
        if y == 0:
            return False
        if x == 0 or x == Cave.WIDTH + 1:
            return False
        if (x, y) in self.filled:
            return False
        return True

    def fix(self, rock, pos):
        for x, y in rock:
            self.filled.add((x + pos[0], y + pos[1]))
            if y + pos[1] > self.top_rock:
                self.top_rock = y + pos[1]

    def is_hit(self, rock, pos, dir):
        for x, y in rock:
            if not self.is_empty(x + pos[0] + dir[0], y + pos[1] + dir[1]):
                return True
        return False

    def get_appeared_pos(self, rock):
        left = min([x for x, y in rock])
        bottom = min([y for x, y in rock])
        return left + 3, self.top_rock - bottom + 4

    def dump(self, rock=None, pos=None):
        for y in range(self.top_rock + 5, -1, -1):
            for x in range(Cave.WIDTH + 2):
                if self.is_empty(x, y):
                    c = '.'
                else:
                    c = '#'
                if rock and pos:
                    for xx, yy in rock:
                        if xx + pos[0] == x and yy + pos[1] == y:
                            c = '@'
                print(c, end='')
            print()
        print('- - - - - - - - - -')

    def copy(self):
        copy = Cave()
        copy.filled = self.filled.copy()
        copy.top_rock = self.top_rock
        return copy


class TestCave:
    def test_cave_walls_and_floor(self):
        sut = Cave()
        # floor
        assert not sut.is_empty(3, 0)
        assert not sut.is_empty(5, 0)

        # wall
        assert not sut.is_empty(0, 1)
        assert not sut.is_empty(8, 1)
        assert not sut.is_empty(0, 11)

        # space
        assert sut.is_empty(1, 1)
        assert sut.is_empty(5, 1000)

    def test_fix_rock(self):
        sut = Cave()
        rock = {(0, 0)}
        sut.fix(rock, pos=(3, 1))
        assert not sut.is_empty(3, 1)
        assert sut.is_empty(2, 1)
        assert sut.is_empty(4, 1)
        assert sut.is_empty(3, 2)

    def test_is_hit(self):
        sut = Cave()
        rock = {(0, 0)}
        assert sut.is_hit(rock, pos=(3, 1), dir=Cave.DOWN)
        assert sut.is_hit(rock, pos=(1, 2), dir=Cave.LEFT)
        assert sut.is_hit(rock, pos=(7, 3), dir=Cave.RIGHT)

    def test_get_appeared_pos(self):
        sut = Cave()
        rock = {(0, 0)}
        assert (3, 4) == sut.get_appeared_pos(rock)

    def test_get_appeared_pos_when_some_rocks_are_fixed(self):
        sut = Cave()
        sut.fix(rock={(0, 0), (0, 1), (0, 2)}, pos=(3, 1))
        rock = {(0, 0)}
        assert (3, 7) == sut.get_appeared_pos(rock)


def move(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]



@dataclass
class Repeat:
    rock: set
    rock_count: int
    pos: tuple
    cave: Cave


def repeating(repeat):
    for y in range(repeat[1].cave.top_rock, 0, -1):
        for yy in range(y - 1, 0, -1):
            if repeat[1].cave.get_line(y) == repeat[1].cave.get_line(yy):
                for i in range(1, yy - y):
                    if repeat[1].cave.get_line(y + i) != repeat[1].cave.get_line(yy + i):
                        break
                else:
                    return True
    pass


def solve(puzzle_input, end_at):
    repeat: dict[int, Repeat] = {}
    rocks = build_rocks(ROCK_PATTERNS)
    winds = [Cave.LEFT if w == '<' else Cave.RIGHT for w in puzzle_input[0]]
    winds_idx = 0
    rock_count = 0
    rock = pos = None
    top_raise = 0

    cave = Cave()
    while True:
        if rock is None:
            rock = rocks[rock_count % len(rocks)]
            rock_count += 1
            pos = cave.get_appeared_pos(rock)

        if winds_idx > 0 and winds_idx % len(winds) == 0:
            if 0 not in repeat:
                repeat[0] = Repeat(rock, rock_count, pos, cave.copy())
            elif 1 not in repeat:
                if repeating(repeat):
                    repeat[1] = Repeat(rock, rock_count, pos, cave.copy())
                    dif = repeat[1].rock_count - repeat[0].rock_count
                    print(repeat)
                    print(dif)
                    rep = (end_at - rock_count) // dif
                    rock_count += dif * rep
                    top_raise = rep * (repeat[1].cave.top_rock - repeat[0].cave.top_rock)

        # wind blows
        wind_dir = winds[winds_idx % len(winds)]
        winds_idx += 1
        if not cave.is_hit(rock, pos, wind_dir):
            pos = move(pos, wind_dir)

        # rock falls
        if not cave.is_hit(rock, pos, Cave.DOWN):
            pos = move(pos, Cave.DOWN)
        else:
            cave.fix(rock, pos)
            if rock_count == end_at:
                break
            rock = pos = None

    return cave.top_rock + top_raise


def test_solve():
    assert solve(['>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'], 2022) == 3068


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input, 2022))


def 問題2(puzzle_input: list[str]):
    print(solve(puzzle_input, 1000000000000))


def main(solve_puzzle1, solve_puzzle2):
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    solve_puzzle1(puzzle_input)
    solve_puzzle2(puzzle_input)


if __name__ == "__main__":
    main(問題1, 問題2)
