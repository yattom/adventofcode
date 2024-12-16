import time
from copy import copy
from typing import TypeAlias
import heapq

Pos: TypeAlias = tuple[int, int]


class Grid:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, pos):
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            return ''
        return self.grid[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        self.grid[y][x] = value

    def __copy__(self):
        return Grid([row[:] for row in self.grid])

    def is_point_on_grid(self, pos: Pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def find(self, char: str) -> Pos | None:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    return x, y
        return None

    def find_all(self, char: str) -> list[Pos]:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    yield x, y

    def dump(self, marks: dict[Pos, str] = None):
        print('-' * 10)
        for y, row in enumerate(self.grid):
            s = ''
            for x, c in enumerate(row):
                if marks and (x, y) in marks:
                    s += marks[x, y]
                else:
                    s += c
            print(s)
        print()


class AmphipodPositions:
    def __init__(self, positions: dict[str, tuple[Pos, ...]], prev=None):
        self.positions = positions
        self.prev = prev
        self.reverse_positions: dict[Pos, str] = {}
        self.key = str(self.positions)
        for kind, pos in self.positions.items():
            for p in pos:
                self.reverse_positions[p] = kind

    def all_positions(self) -> list[Pos]:
        return list(self.reverse_positions.keys())

    def get_all(self) -> list[str, Pos]:
        for kind, positions in self.positions.items():
            for pos in positions:
                yield kind, pos

    def get_at(self, pos: Pos) -> str | None:
        return self.reverse_positions.get(pos, None)

    def move(self, kind: str, pos: Pos, new_pos: Pos):
        '''
        return a new AmphipodPositions object with the specified amphipod moved to the new position
        :param kind:
        :param pos:
        :param new_pos:
        :return:
        '''
        new_positions = copy(self.positions)
        new_positions[kind] = tuple(new_pos if p == pos else p for p in new_positions[kind])
        return AmphipodPositions(new_positions, prev=self)

    def __repr__(self):
        return f'AmphipodPositions({str(self.positions)})'

    def dump(self, burrow=None):
        if burrow:
            width, height = burrow.grid.width, burrow.grid.height
        else:
            width, height = 12, 4
        for y in range(height):
            for x in range(width):
                kind = self.get_at((x, y))
                if kind:
                    print(kind, end='')
                else:
                    print('.', end='')
            print()
        print()

    def __lt__(self, other):
        return self.key < other.key


class Burrow:
    HALLWAY_Y = 1

    def __init__(self, grid: Grid):
        self.grid = grid
        self.free_spots: list[tuple[int, int]] = list(grid.find_all('.'))
        self.free_spots.remove((3, 1))
        self.free_spots.remove((5, 1))
        self.free_spots.remove((7, 1))
        self.free_spots.remove((9, 1))

        self.initial_amphipods = AmphipodPositions({
            'A': tuple(grid.find_all('A')),
            'B': tuple(grid.find_all('B')),
            'C': tuple(grid.find_all('C')),
            'D': tuple(grid.find_all('D')),
        })

        self.rooms: list[Pos] = []
        for pos in self.initial_amphipods.all_positions():
            self.rooms.append(pos)
        # goal_rooms[kind] is a list of positions of kind rooms
        # it is guaranteed that goal_rooms[kind][0] is y == 2 and [1] is y == 3
        self.goal_rooms: dict[str, list[Pos]] = {
            'A': sorted([pos for pos in self.rooms if pos[0] == 3]),
            'B': sorted([pos for pos in self.rooms if pos[0] == 5]),
            'C': sorted([pos for pos in self.rooms if pos[0] == 7]),
            'D': sorted([pos for pos in self.rooms if pos[0] == 9]),
        }

    def dump(self):
        print(f'{self.free_spots=}')
        print(f'{self.initial_amphipods=}')
        print(f'{self.rooms=}')
        print(f'{self.goal_rooms=}')


ENERGY_PER_STEP = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def parse_as_grid(lines: list[str]):
    return Grid([list(line.strip('\n')) for line in lines])


def path(start: Pos, goal: Pos, burrow: Burrow, amphipods: AmphipodPositions) -> list[Pos] | None:
    '''
    path does not include the start position and does include the goal position

    :param self:
    :param start:
    :param goal:
    :param burrow:
    :param amphipods:
    :return:
    '''
    if start == goal:
        raise RuntimeError('0 step movement is not allowed')

    def go_up_out() -> list[Pos]:
        return [(start[0], y) for y in range(start[1] - 1, Burrow.HALLWAY_Y - 1, -1)]

    def go_down_in() -> list[Pos]:
        return [(goal[0], y) for y in range(Burrow.HALLWAY_Y + 1, goal[1] + 1)]

    def go_sideways() -> list[Pos]:
        if goal[0] > start[0]:
            return [(x, Burrow.HALLWAY_Y) for x in range(start[0] + 1, goal[0] + 1)]
        else:
            return [(x, Burrow.HALLWAY_Y) for x in range(start[0] - 1, goal[0] - 1, -1)]

    if start in burrow.rooms and goal in burrow.free_spots:
        up = go_up_out()
        side = go_sideways()
        candidate = up + side
    elif start in burrow.free_spots and goal in burrow.rooms:
        side = go_sideways()
        down = go_down_in()
        candidate = side + down
    elif start in burrow.rooms and goal in burrow.rooms:
        up = go_up_out()
        side = go_sideways()
        down = go_down_in()
        candidate = up + side + down
    else:
        raise RuntimeError('Invalid start and goal positions')

    for pos in candidate:
        if amphipods.get_at(pos) is not None:
            return None
    return candidate


def possible_goals(start: Pos, kind: str, burrow: Burrow, amphipods: AmphipodPositions) -> list[Pos]:
    rooms = burrow.goal_rooms[kind]
    # print(f'{start=}, {rooms=}, {amphipods.get_at(rooms[0])=}, {amphipods.get_at(rooms[1])=}')

    p = []
    if start in rooms:
        # if the amphipod is already in the goal room, and only the same kind are in the room, it cannot move
        for pos in rooms[::-1]:
            if amphipods.get_at(pos) != kind:
                # there are other kinds below so it can move
                break
            if pos == start:
                # already in the goal room; cannot move
                return []
        else:
            raise RuntimeError('should not come here')
    else:
        # goal can be in the room; find the appropriate position
        for pos in rooms[::-1]:
            a = amphipods.get_at(pos)
            if a == kind:
                # same kind here; find a position above
                continue
            elif a is None:
                # an empty pos; can be moved here
                # ignore any other positions above in the room; path() will handle the situation
                p += [pos]
                # uncomment 'return p' and get a wrong answer
                # returning here means when the amphipod can move directly into the goal room, it doesn't need to
                #  try moving into hallway.  I cannot see why this is wrong.
                # return p
                break
            elif a != kind:
                # other kind here; cannot move
                break

    # direct movement into a goal is no possible; move to one of the free spots
    if start not in burrow.free_spots:
        return p + [pos for pos in burrow.free_spots if pos not in amphipods.all_positions()]
    return p + []


def is_everyone_in_their_rooms(amphipods: AmphipodPositions, burrow: Burrow):
    for kind, pos in amphipods.get_all():
        if pos not in burrow.goal_rooms[kind]:
            return False
    return True


class DebugPrinter:
    def __init__(self, enabled=False, interval=0):
        self.enabled = enabled
        self.interval = interval
        if self.interval:
            self.start_ns = time.time_ns()
            self.last_ns = self.start_ns

    def print(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)

    def at_interval(self) -> bool:
        if not self.enabled or not self.interval:
            return False
        if time.time_ns() - self.last_ns > self.interval:
            self.last_ns += self.interval
            return True

    def elapsed(self):
        return (time.time_ns() - self.start_ns) / (1000 * 1000 * 1000)


def puzzle1(lines: list[str]):
    burrow = Burrow(parse_as_grid(lines))
    burrow.dump()
    least_energy = 9999999999
    least_solution = None

    dp = DebugPrinter(enabled=True, interval=3 * 1000 * 1000 * 1000)
    states: list[tuple[int, AmphipodPositions]] = []
    heapq.heappush(states, (0, burrow.initial_amphipods))
    visited: set[str] = set()
    while states:
        energy, amphipods = heapq.heappop(states)
        if dp.at_interval():
            print(f'{energy=}, {len(states)}, at {dp.elapsed()}s')
        if amphipods.key in visited:
            continue
        if is_everyone_in_their_rooms(amphipods, burrow):
            print(f'solved with {energy=}')
            if energy < least_energy:
                least_energy = energy
                least_solution = amphipods
                print(f'least energy: {least_energy}')
                continue
        visited.add(amphipods.key)
        for kind, pos in amphipods.get_all():
            goals = possible_goals(pos, kind, burrow, amphipods)
            for g in goals:
                p = path(pos, g, burrow, amphipods)
                if not p:
                    continue
                new_amphipods = amphipods.move(kind, pos, g)
                # amphipods.dump()
                # print(f'vvvvvvvv {energy}->{energy + ENERGY_PER_STEP[a[0]] * len(p)}')
                # new_amphipods.dump()
                heapq.heappush(states, (energy + ENERGY_PER_STEP[kind] * len(p), new_amphipods))


    solution = []
    a = least_solution
    while a is not None:
        solution.insert(0, a)
        a = a.prev
    for a in solution:
        a.dump(burrow)
    return least_energy


def puzzle2(lines: list[str]):
    lines = lines[0:3] + [
        '  #D#C#B#A#',
        '  #D#B#A#C#',
    ] + lines[3:]
    return puzzle1(lines)


def main():
    import sys
    if len(sys.argv) == 1:
        lines = sys.stdin.readlines()
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    print(puzzle1(lines))
    print(puzzle2(lines))


if __name__ == "__main__":
    main()
