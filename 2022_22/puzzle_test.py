import pytest

from puzzle import *


@pytest.fixture
def sample_input():
    return [
        "        ...#",
        "        .#..",
        "        #...",
        "        ....",
        "...#.......#",
        "........#...",
        "..#....#....",
        "..........#.",
        "        ...#....",
        "        .....#..",
        "       .#......",
        "        ......#.",
        "",
        "10R5L5R10L4R5L5",
    ]

def test_parse(sample_input):
    board, instructions = parse(sample_input)
    assert board.is_floor((1, 9))
    assert board.is_wall((2, 10))
    assert board.is_off((9, 1))
    assert board.width == 16
    assert board.height == 12
    assert instructions == [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]


def test_outside_of_board(sample_input):
    board, _ = parse(sample_input)
    assert board.is_off((0, 1))
    assert board.is_off((1, 0))
    assert board.is_off((9, 17))
    assert board.is_off((13, 10))


def test_start_loc(sample_input):
    board, _ = parse(sample_input)
    sut = Counter(board)
    assert sut.loc == (1, 9)
    assert sut.facing == (0, 1)


def test_step_forward(sample_input):
    board, _ = parse(sample_input)
    marker = Counter(board)
    marker.forward(1)
    assert marker.loc == (1, 10)


def test_step_forward_to_be_blocked(sample_input):
    board, _ = parse(sample_input)
    counter = Counter(board)
    counter.forward(5)
    assert counter.loc == (1, 11)


def test_step_forward_to_warp(sample_input):
    board, _ = parse(sample_input)
    counter = Counter(board)
    counter.loc = (5, 5)
    counter.facing = (-1, 0)
    counter.forward(3)
    assert counter.loc == (6, 5)


def test_step_forward_to_warp_to_be_blocked(sample_input):
    board, _ = parse(sample_input)
    counter = Counter(board)
    counter.loc = (1, 11)
    counter.facing = (0, -1)
    counter.forward(5)
    assert counter.loc == (1, 9)


def test_turn_right(sample_input):
    board, _ = parse(sample_input)
    counter = Counter(board)
    counter.turn("R")
    assert counter.facing == (1, 0)


def test_turn_left(sample_input):
    board, _ = parse(sample_input)
    counter = Counter(board)
    counter.turn("L")
    assert counter.facing == (-1, 0)


def test_score():
    board = Board(["..#", ".#.", "..."])
    counter = Counter(board)
    counter.loc = (6, 8)
    counter.facing = (0, 1)
    assert score(counter) == 6032


def test_solve(sample_input):
    assert solve(sample_input) == 6032


