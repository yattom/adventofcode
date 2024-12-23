from puzzle import *
import pytest

def test_calculate_sequence_for_robot_on_keypad1():
    state = State()
    actual = calculate_sequence_for_robot_on_keypad1(state, NUMPAD['0'])
    assert actual == '<A'
    assert state.robot_at_numpad == NUMPAD['0']


def test_shortest_sequence():
    actual = shortest_sequence(start=NUMPAD['A'], target=NUMPAD['0'], target_pad=NUMPAD)
    assert actual == '<A'

def test_calculate_sequence_for_robot_on_keypad2():
    state = State()
    state.robot_at_numpad = Pos(1, 0)
    actual = calculate_sequence_for_robot_on_keypad2(state, KEYPAD['<'])
    assert actual == 'v<<A'
    assert state.robot_at_keypad1 == KEYPAD['<']


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
    actual = shortest_sequence_set_for_you(NUMPAD['A'], NUMPAD['2'])
    assert '<vA<AA>>^AvA<^A>AvA^A' in actual