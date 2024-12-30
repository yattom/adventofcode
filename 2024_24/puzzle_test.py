import pytest
from puzzle import *


def test_all_combination_of_pairs():
    assert sorted(list(all_combination_of_pairs(2, 4))) == [
        ((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))
    ]


@pytest.mark.parametrize(
    "num_choices,num_items,expected",
    [
        (2, 3, [[0, 1], [0, 2], [1, 2]]),
        (4, 4, [[0, 1, 2, 3]]),
        (4, 5, [[0, 1, 2, 3], [0, 1, 2, 4], [0, 1, 3, 4], [0, 2, 3, 4], [1, 2, 3, 4]]),
    ]

)
def test_combinations(num_choices, num_items, expected):
    assert sorted(list(combinations(num_choices, num_items))) == expected


def test_permutations():
    assert sorted(permutations([1, 2, 3])) == sorted([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    assert len(permutations([i for i in range(8)])) == 40320


@pytest.fixture
def puzzle():
    x_labels = [f'x{n:02d}' for n in range(10)][::-1]
    y_labels = [f'y{n:02d}' for n in range(10)][::-1]
    z_labels = [f'z{n:02d}' for n in range(10)][::-1]
    labels = set(x_labels + y_labels + z_labels)
    values = {}
    puzzle = Puzzle({}, values, labels, x_labels, y_labels, z_labels)
    return puzzle


def test_bits(puzzle: Puzzle):
    values = {'z00': 0, 'z01': 0, 'z02': 1, 'z03': 0, 'z04': 0, 'z05': 1, 'z06': 0, 'z07': 0, 'z08': 0, 'z09': 1}
    actual_z_bits = calc_bits(values, puzzle.z_labels)
    assert actual_z_bits == '1000100100'


def test_is_valid_pairs():
    puzzle = Puzzle.build_puzzle([
        'x00: 0',
        'y00: 0',
        'x01: 0',
        'y01: 0',
        '',
        'x00 XOR y00 -> z00',
        # 'x00 AND y00 -> aaa',
        # 'x01 XOR y01 -> bbb',
        # 'aaa XOR bbb -> z01',
        # 'aaa AND bbb -> ccc',
        # 'x01 AND y01 -> ddd',
        # 'ccc AND ddd -> z02',
    ])
    working = Working()
    assert is_valid_pairs(puzzle, working, (()))


def test_set_x_y_value():
    puzzle = Puzzle.build_puzzle([
        'x00: 0',
        'y00: 0',
        'x01: 0',
        'y01: 0',
        'x02: 0',
        'y02: 0',
        '',
        'x00 XOR y00 -> z00',
    ])
    values = {}
    set_x_y_values(values, puzzle.x_labels, puzzle.y_labels, x=2, y=6)
    assert values['x00'] == 0
    assert values['x01'] == 1
    assert values['x02'] == 0
    assert values['y00'] == 0
    assert values['y01'] == 1
    assert values['y02'] == 1
