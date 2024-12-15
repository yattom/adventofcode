from pytest import fixture, mark
from puzzle import Burrow, Grid, parse_as_grid, possible_goals, AmphipodPositions, Pos, path


@fixture
def burrow():
    return Burrow(parse_as_grid([
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #B#C#A#D#',
        '  #########',
    ]))


@fixture
def burrow4():
    return Burrow(parse_as_grid([
        '#############',
        '#...........#',
        '###A#B#C#D###',
        '  #D#C#B#A#',
        '  #D#B#A#C#',
        '  #B#C#A#D#',
        '  #########',
    ]))


def build_amphipods(lines) -> AmphipodPositions:
    amphipods: dict[str, tuple[Pos, ...]] = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                if char not in amphipods:
                    amphipods[char] = []
                amphipods[char].append((x, y))
    return AmphipodPositions(amphipods)


@mark.parametrize("start_pos, amphipod", [
    ((3, 3), 'A'),
    ((9, 2), 'D'),
    ((9, 3), 'D'),
])
def test_possible_goal_cannot_get_out(burrow, start_pos, amphipod):
    amphipods = build_amphipods([
        '............',
        '..A...C....B',
        '.....B...D..',
        '...A.C...D..',
    ])
    assert possible_goals(start_pos, amphipod, burrow, amphipods) == []


@mark.parametrize("start_pos, amphipod", [
    ((5, 2), 'B'),
    ((7, 3), 'B'),
])
def test_possible_goal_can_get_out(burrow, start_pos, amphipod):
    amphipods = build_amphipods([
        '............',
        '..A...C.....',
        '.....B...D..',
        '...A.C.B.D..',
    ])
    assert (1, 1) in possible_goals(start_pos, amphipod, burrow, amphipods)


@mark.parametrize("start_pos, amphipod", [
    ((2, 1), 'A'),
])
def test_possible_goal_cannot_go_sideways(burrow, start_pos, amphipod):
    amphipods = build_amphipods([
        '............',
        '..A...C....B',
        '...B.....D..',
        '...A.C...D..',
    ])
    assert possible_goals(start_pos, amphipod, burrow, amphipods) == []


@mark.parametrize("start_pos, amphipod", [
    ((11, 1), 'B'),
])
def test_possible_goal_cannot_go_in_occupied_room(burrow, start_pos, amphipod):
    amphipods = build_amphipods([
        '............',
        '..A...C....B',
        '...B.....D..',
        '...A.C...D..',
    ])
    assert possible_goals(start_pos, amphipod, burrow, amphipods) == []


@mark.parametrize("start_pos, amphipod, goal", [
    ((3, 1), 'B', (5, 3)),
])
def test_possible_goal_can_go_out_then_in(burrow, start_pos, amphipod, goal):
    amphipods = build_amphipods([
        '............',
        '..A...C....B',
        '...B.....D..',
        '...A...C.D..',
    ])
    assert goal in possible_goals(start_pos, amphipod, burrow, amphipods)


def test_path_blocked(burrow):
    amphipods = build_amphipods([
        '............',
        '..A.A.B.....',
        '.......C.D..',
        '...B...C.D..',
    ])
    assert path((3, 3), (5, 3), burrow, amphipods) is None


@mark.parametrize("start_pos, amphipod, goal_pos, steps", [
    ((2, 1), 'A', (3, 2), 2),
    ((7, 2), 'B', (5, 3), 5),
    ((11, 1), 'B', (5, 3), 8),
    ((9, 5), 'D', (6, 1), 7),
])
def test_path_room_of_4positions(burrow4, start_pos, amphipod, goal_pos, steps):
    amphipods = build_amphipods([
        '............',
        '..A.C......B',
        '.......B....',
        '...A...C....',
        '...A.B.C....',
        '...A.B.C.D..',
    ])
    assert len(path(start_pos, goal_pos, burrow4, amphipods)) == steps


@mark.parametrize("start_pos, amphipod", [
    # ((3, 5), 'A'),  # A cannot go out
    ((5, 4), 'B'),
    ((7, 3), 'C'),
    ((9, 2), 'D'),
])
def test_possible_goal_depth4_can_go_out_to_hallway(burrow4, start_pos, amphipod):
    amphipods = build_amphipods([
        '............',
        '............',
        '.........D..',
        '.......C.D..',
        '.....B.C.D..',
        '...A.A.A.A..',
    ])
    assert possible_goals(start_pos, amphipod, burrow4, amphipods)[0][1] == Burrow.HALLWAY_Y
    assert len(possible_goals(start_pos, amphipod, burrow4, amphipods)) == 7
    assert possible_goals(start_pos, amphipod, burrow4, amphipods) \
           == [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)]


@mark.parametrize("start_pos, amphipod, goal_pos, length", [
    ((3, 5), 'B', (1, 1), 6),
    ((3, 5), 'B', (5, 3), 8),
    ((11, 1), 'C', (7, 5), 8),
])
def test_path_depth4(burrow4, start_pos, amphipod, goal_pos, length):
    amphipods = build_amphipods([
        '............',
        '...........C',
        '.........D..',
        '.........D..',
        '.....B...D..',
        '...B.B...A..',
    ])
    assert len(path(start_pos, goal_pos, burrow4, amphipods)) == length


@mark.parametrize("start_pos, amphipod, goal_pos", [
    ((5, 2), 'C', (7, 5)),
    ((5, 2), 'C', (6, 1)),
])
def test_possible_goal_depth4(burrow4, start_pos, amphipod, goal_pos):
    amphipods = build_amphipods([
        '.............',
        '.AA.....B.C..',
        '...A.C...D...',
        '...D.C...A...',
        '...D.B...C...',
        '...B.D...B...',
    ])
    assert goal_pos in possible_goals(start_pos, amphipod, burrow4, amphipods)
