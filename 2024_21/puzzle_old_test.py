import pytest
from puzzle_old import *


@pytest.mark.parametrize(
    'target,expected',
    [
        ('0', {'<A'}),
        ('1', {'<^<A', '^<<A'}),
        ('7', {'^^^<<A', '^^<^<A', '^^<<^A', '^<^^<A', '^<^<^A', '^<<^^A', '<^^^<A', '<^^<^A', '<^<^^A'}),
    ]
)
def test_get_sequence_to_push_button(target, expected):
    seq = get_sequence_to_push_button(NUMPAD['A'], NUMPAD[target], NUMPAD, KEYPAD)
    assert seq[1] == expected


@pytest.mark.parametrize(
    'target,expected',
    [
        ('0A', {'<A>A'}),
        ('15', {'<^<A>^A', '^<<A>^A', '<^<A^>A', '^<<A^>A'}),
        ('012', {'<A^<A>A'}),
        ('029A', {'<A^A^>^AvvvA', '<A^A>^^AvvvA', '<A^A^^>AvvvA'}),
        ('7', {'^^^<<A', '^^<^<A', '^^<<^A', '^<^^<A', '^<^<^A', '^<<^^A', '<^^^<A', '<^^<^A', '<^<^^A'}),
    ]
)
def test_get_sequence_for_sequence(target, expected):
    seq = get_sequence_for_sequence(NUMPAD['A'], {target}, NUMPAD, KEYPAD)
    assert seq == expected
@pytest.mark.parametrize(
    'target,expected',
    [
        ('<A^A^>^AvvvA', set()),
        ('<A^A>^^AvvvA', set()),
        ('<A^A^^>AvvvA', set()),
    ]
)
def test_get_sequence_for_sequence_for_keypad(target, expected):
    seq = get_sequence_for_sequence(NUMPAD['A'], {target}, KEYPAD, KEYPAD)
    assert seq == expected
