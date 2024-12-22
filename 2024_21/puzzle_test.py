from puzzle import *

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

def test_calculate_sequence_for_robot_on_keypad2_length_differ():
    state = State()
    state.robot_at_numpad = NUMPAD['3']
    s1 = ''
    for c in '<<^A':
        s1 += calculate_sequence_for_robot_on_keypad2(state, KEYPAD[c])

    s2 = ''
    for c in '<^<A':
        s2 += calculate_sequence_for_robot_on_keypad2(state, KEYPAD[c])

    assert s1 == s2

