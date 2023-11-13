import pytest
from dataclasses import dataclass
import time


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return self.y * 10000 + self.x
    
    def __add__(self, other):
        assert type(other) == Vector
        return Point(self.x + other.dx, self.y + other.dy)


@dataclass
class Vector:
    dx: int
    dy: int


RIGHT = Vector(1, 0)
LEFT = Vector(-1, 0)
UP = Vector(0, -1)
DOWN = Vector(0, 1)
WAIT = Vector(0, 0)
WIND_CHARS = {
    '>': RIGHT,
    '<': LEFT,
    '^': UP,
    'v': DOWN,
}


@dataclass
class Wind:
    point: Point
    vector: object



class Valley:
    @staticmethod
    def parse(puzzle_input):
        valley = Valley()
        valley.width = len(puzzle_input[0])
        valley.height = len(puzzle_input)
        valley.map = {}
        valley.winds = []
        for y, l in enumerate(puzzle_input):
            for x, c in enumerate(l):
                if c == '#':
                    valley.map[Point(x=x, y=y)] = c
                else:
                    if c in WIND_CHARS:
                        valley.winds.append(Wind(Point(x, y), WIND_CHARS[c]))
                        valley.map[Point(x=x, y=y)] = 'w'
                    else:
                        valley.map[Point(x=x, y=y)] = '.'

        valley.start = Point(x=1, y=0)
        valley.goal = Point(x=valley.width - 2, y=valley.height - 1)
        return valley

    def is_clear(self, point):
        return self.map[point] == '.'

    def is_wall(self, point):
        return self.map[point] == '#'

    def next_wind(self, wind):
        new_point = wind.point + wind.vector
        if self.is_wall(new_point):
            if wind.vector == RIGHT:
                new_point = Point(1, new_point.y)
            elif wind.vector == LEFT:
                new_point = Point(self.width - 2, new_point.y)
            elif wind.vector == UP:
                new_point = Point(new_point.x, self.height - 2)
            elif wind.vector == DOWN:
                new_point = Point(new_point.x, 1)
        return Wind(new_point, wind.vector)

    def generate_next(self):
        valley = Valley()
        valley.width = self.width
        valley.height = self.height
        valley.winds = [self.next_wind(w) for w in self.winds]
        valley.map = {}
        for p, c in self.map.items():
            if c == '#':
                valley.map[p] = c
            else:
                valley.map[p] = '.'
        for w in valley.winds:
            valley.map[w.point] = 'w'

        return valley


class ValleyHistory:
    def __init__(self, init):
        self.init = init
        self.history = [init]
        self.repeat = (init.width - 2) * (init.height - 2)

    def __getitem__(self, idx):
        if self.repeat > 0:
            idx = idx % self.repeat
        if idx <= len(self.history) - 1:
            return self.history[idx]
        for i in range(len(self.history), idx + 1):
            new_valley = self.history[i - 1].generate_next()
            self.history.append(new_valley)
        return new_valley


@pytest.fixture
def empty_valley():
    puzzle_input = [
        "#.########",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "########.#",
    ]
    return Valley.parse(puzzle_input)


@pytest.fixture
def some_winds():
    puzzle_input = [
            "#.########",
            "#.>......#",
            "#......<.#",
            "#...v....#",
            "#........#",
            "#......^.#",
            "########.#",
    ]
    return Valley.parse(puzzle_input)


def test_next_wind(empty_valley):
    wind = Wind(Point(3, 3), DOWN)
    new_wind = empty_valley.next_wind(wind)
    assert new_wind.point == Point(3, 4)


def test_next_wind_across(empty_valley):
    wind = Wind(Point(8, 3), RIGHT)
    new_wind = empty_valley.next_wind(wind)
    assert new_wind.point == Point(1, 3)


class TestValley:
    def test_empty(self):
        puzzle_input = [
            "#.########",
            "#........#",
            "#........#",
            "#........#",
            "#........#",
            "#........#",
            "########.#",
        ]
        valley = Valley.parse(puzzle_input)
        assert valley.width == 10
        assert valley.height == 7
        assert valley.start == Point(x=1, y=0)
        assert valley.goal == Point(x=8, y=6)
        assert len(valley.winds) == 0

    def test_some_winds(self):
        puzzle_input = [
            "#.########",
            "#.>......#",
            "#......<.#",
            "#...v....#",
            "#........#",
            "#.......^#",
            "########.#",
        ]
        valley = Valley.parse(puzzle_input)
        assert len(valley.winds) == 4
        assert valley.winds[0] == Wind(Point(2, 1), RIGHT)
        assert valley.winds[1] == Wind(Point(7, 2), LEFT)
        assert valley.winds[2] == Wind(Point(4, 3), DOWN)
        assert valley.winds[3] == Wind(Point(8, 5), UP)

    def test_is_clear(self):
        puzzle_input = [
            "#.########",
            "#.>......#",
            "#......<.#",
            "#...v....#",
            "#........#",
            "#......^.#",
            "########.#",
        ]
        valley = Valley.parse(puzzle_input)
        assert not valley.is_clear(Point(0, 0))
        assert valley.is_clear(Point(1, 0))
        assert valley.is_clear(Point(1, 1))
        assert not valley.is_clear(Point(2, 1))


class TestValleyHistory:
    def test_no_winds(self, empty_valley):
        sut = ValleyHistory(empty_valley)
        assert sut[0].winds == sut[3].winds

    def test_some_winds_generate_next(self, some_winds):
        sut = ValleyHistory(some_winds)
        assert sut[0].winds != sut[3].winds

    def test_some_winds_repeat(self, some_winds):
        sut = ValleyHistory(some_winds)
        assert sut[0].winds == sut[(10 - 2) * (7 - 2)].winds
        assert sut.repeat == (10 - 2) * (7 - 2)

    def test_some_winds_no_calculation_after_repeat(self, some_winds):
        sut = ValleyHistory(some_winds)
        assert sut[1].winds == sut[(10 - 2) * (7 - 2) + 1].winds
        assert len(sut.history) < (10 - 2) * (7 - 2) + 1


def shortest_path_with_eval(valley, start_time, start, goal):
    def score(e):
        step_count, p = e
        return (abs(goal.x - p.x) + abs(goal.y - p.y)) + step_count
    touched = set()
    points_to_check = [(score((start_time, start)), start_time, start)]
    history = ValleyHistory(valley)
    start_t = perf_t = time.perf_counter()
    log_interval = 0
    while points_to_check:
        # print(points_to_check)
        if log_interval % 1000 == 0:
            print(f"{len(points_to_check)=} elapsed={time.perf_counter() - start_t:.2f} interval={time.perf_counter() - perf_t:.2f}")
            print(points_to_check[:10])
            perf_t = time.perf_counter()
        log_interval += 1
        _, step_count, point = points_to_check.pop(0)
        current_valley = history[step_count + 1]
        if point == goal:
            return step_count
        for v in [LEFT, RIGHT, UP, DOWN, WAIT]:
            p = point + v
            if p.y < 0 or p.y >= valley.height or not current_valley.is_clear(p):
                continue
            if (step_count + 1, p) in touched:
                continue
            points_to_check.append((score((step_count + 1, p)), step_count + 1, p))
            points_to_check.sort(key=lambda e: e[0])
            touched.add((step_count + 1, p))


def shortest_path(valley, start_time, start, goal):
    touched = set()
    points_to_check = [(start_time, start)]
    history = ValleyHistory(valley)
    start_t = perf_t = time.perf_counter()
    log_interval = 0
    while points_to_check:
        # print(points_to_check)
        if log_interval % 1000 == 0:
            print(f"{len(points_to_check)=} elapsed={time.perf_counter() - start_t:.2f} interval={time.perf_counter() - perf_t:.2f}")
            print(points_to_check[:10])
            perf_t = time.perf_counter()
        log_interval += 1
        step_count, point = points_to_check.pop(0)
        current_valley = history[step_count + 1]
        if point == goal:
            return step_count
        for v in [LEFT, RIGHT, UP, DOWN, WAIT]:
            p = point + v
            if p.y < 0 or p.y >= valley.height or not current_valley.is_clear(p):
                continue
            if (step_count + 1, p) in touched:
                continue
            points_to_check.append((step_count + 1, p))
            touched.add((step_count + 1, p))


def test_shortest_path():
    puzzle_input = [
        "#.######",
        "#>>.<^<#",
        "#.<..<<#",
        "#>v.><>#",
        "#<^v^^>#",
        "######.#",
    ]
    valley = Valley.parse(puzzle_input)
    assert shortest_path(valley, 0, valley.start, valley.goal) == 18


def test_shortest_path_with_eval():
    puzzle_input = [
        "#.######",
        "#>>.<^<#",
        "#.<..<<#",
        "#>v.><>#",
        "#<^v^^>#",
        "######.#",
    ]
    valley = Valley.parse(puzzle_input)
    assert shortest_path_with_eval(valley, 0, valley.start, valley.goal) == 18

def test_solve2():
    puzzle_input = [
        "#.######",
        "#>>.<^<#",
        "#.<..<<#",
        "#>v.><>#",
        "#<^v^^>#",
        "######.#",
    ]
    assert solve2(puzzle_input) == 54


def solve(puzzle_input):
    valley = Valley.parse(puzzle_input)
    return shortest_path_with_eval(valley, 0, valley.start, valley.goal)


def solve2(puzzle_input):
    valley = Valley.parse(puzzle_input)
    to_goal = shortest_path_with_eval(valley, 0, valley.start, valley.goal)
    back_to_start = shortest_path_with_eval(valley, to_goal, valley.goal, valley.start)
    to_goal_again = shortest_path_with_eval(valley, back_to_start, valley.start, valley.goal)
    return to_goal_again


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    pass  # print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
