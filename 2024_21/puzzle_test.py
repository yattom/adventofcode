from puzzle import *
import pytest


@pytest.mark.parametrize("start, target, expected", [
    (NUMPAD['A'], NUMPAD['0'], {'<A'}),
    (NUMPAD['1'], NUMPAD['3'], {'>>A'}),
    (NUMPAD['2'], NUMPAD['5'], {'^A'}),
    (NUMPAD['A'], NUMPAD['5'], {'^^<A', '<^^A'}),
    (NUMPAD['A'], NUMPAD['4'], {'^^<<A'}),
])
def test_shortest_sequence_set(start, target, expected):
    actual = get_sequence_set(start=start, target=target, target_pad=NUMPAD)
    assert actual == expected


def test_shortest_sequence_set_for_you():
    actual = shortest_sequence_set_for_you(NUMPAD['A'], NUMPAD['2'], 2)
    assert '<vA<AA>>^AvA<^A>AvA^A' in actual


def test_calc_smallest_number_of_sequence_for_keypad():
    nth_0 = {(start, target): 1 for start in KEYPAD if start != GAP for target in KEYPAD if target != GAP}
    nth_1 = calc_smallest_number_of_sequence_for_keypad(nth_0)
    assert nth_1[('A', '<')] == 4
    assert nth_1[('A', '^')] == 2
    assert nth_1[('A', 'v')] == 3
    assert nth_1[('A', '>')] == 2
    assert nth_1[('A', 'A')] == 1
    nth_2 = calc_smallest_number_of_sequence_for_keypad(nth_1)
    assert nth_2[('A', '<')] == 10
    assert nth_2[('A', '^')] == 8
    assert nth_2[('A', 'v')] == 9
    assert nth_2[('A', '>')] == 6
    assert nth_2[('A', 'A')] == 1
