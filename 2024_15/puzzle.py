import time
from typing import TypeAlias

Pos: TypeAlias = tuple[int, int]


class Grid:
    NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __getitem__(self, pos):
        x, y = pos
        if not self.is_point_on_grid(pos):
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

    def __iter__(self):
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                yield (x, y), c


def parse_as_grid(lines: list[str]):
    return Grid([list(line.strip('\n')) for line in lines])


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


VECTORS = {
    '<': (-1, 0),
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
}


def puzzle1(lines: list[str]):
    sep = [l.strip() for l in lines].index('')
    grid = parse_as_grid(lines[:sep])
    walls = set(grid.find_all('#'))
    boxes = set(grid.find_all('O'))
    robot_pos = grid.find('@')
    instructions = ''.join([l.strip() for l in lines[sep + 1:]])

    def can_advance(pos: Pos, dx: int, dy: int):
        '''
        return True if the robot can advance in the direction dx, dy.
        Which is either:
        - the next position is open (neither a wall nor a box)
        - the next position is a box and you can push the box (and all the boxes behind it)
        :param pos:
        :param dx:
        :param dy:
        :return:
        '''
        new_pos = pos[0] + dx, pos[1] + dy
        if new_pos in walls:
            return False
        if not new_pos in boxes:
            return True
        # let's see if we can push the box
        pos_to_check = new_pos
        while True:
            if not grid.is_point_on_grid(pos_to_check):
                # this is unnecessary as the walls surround the grid
                return False
            if pos_to_check in walls:
                return False
            if pos_to_check not in boxes:
                return True
            # pos in boxes
            pos_to_check = pos_to_check[0] + dx, pos_to_check[1] + dy

    def advance(pos: Pos, dx: int, dy: int):
        box_pos = first_box_pos = pos[0] + dx, pos[1] + dy
        if box_pos not in boxes:
            pass
        else:
            while True:
                if not grid.is_point_on_grid(box_pos):
                    # this is unnecessary as the walls surround the grid
                    return False
                if box_pos in walls:
                    raise ValueError('Cannot advance into a wall')
                if box_pos not in boxes:
                    break
                box_pos = box_pos[0] + dx, box_pos[1] + dy
            # note that you really don't need to change all the boxes;
            # just take the first one and move it to the far end position
            boxes.remove(first_box_pos)
            boxes.add(box_pos)
        return first_box_pos  # this is the new robot position

    for dx, dy in [VECTORS[c] for c in instructions]:
        if can_advance(robot_pos, dx, dy):
            robot_pos = advance(robot_pos, dx, dy)

    gps_score = sum([x + y * 100 for (x, y) in boxes])
    return gps_score


def puzzle2(lines: list[str]):
    sep = [l.strip() for l in lines].index('')
    grid = parse_as_grid(lines[:sep])
    walls = set()
    for wx, wy in grid.find_all('#'):
        walls.add((wx * 2, wy))
        walls.add((wx * 2 + 1, wy))
    boxes = set([(x * 2, y) for (x, y) in grid.find_all('O')])
    robot_pos = (grid.find('@')[0] * 2, grid.find('@')[1])
    instructions = ''.join([l.strip() for l in lines[sep + 1:]])

    def hit_box(pos: Pos):
        for bx, by in boxes:
            if pos == (bx, by) or pos == (bx + 1, by):
                return (bx, by)
        return None

    def can_advance(pos: Pos, dx: int, dy: int):
        '''
        return True if the robot can advance in the direction dx, dy.
        Which is either:
        - the next position is open (neither a wall nor a box)
        - the next position is a box and you can push the box (and all the boxes behind it)
        :param pos:
        :param dx:
        :param dy:
        :return:
        '''
        new_pos = pos[0] + dx, pos[1] + dy
        if new_pos in walls:
            return False
        pos_to_check = {new_pos}
        while True:
            if not all([(0 <= p[0] < grid.width * 2 and 0 <= p[1] < grid.height) for p in pos_to_check]):
                # this is unnecessary as the walls surround the grid
                return False
            if any([(p in walls) for p in pos_to_check]):
                return False
            if all([hit_box(p) is None for p in pos_to_check]):
                return True
            # some pos_to_check in boxes
            next_pos_to_check = set()
            for p in pos_to_check:
                if (b := hit_box(p)) is not None:
                    bx, by = b
                    if dy == 0:
                        # horizontal; need to check 2 cells away
                        next_pos_to_check.add((p[0] + dx * 2, p[1]))
                    elif dx == 0:
                        # vertical; need to check 2 cells width
                        next_pos_to_check.add((bx, by + dy))
                        next_pos_to_check.add((bx + 1, by + dy))
                    else:
                        raise ValueError('Cannot push a box diagonally')
            pos_to_check = next_pos_to_check

    def boxes_to_push(pos: Pos, dx: int, dy: int):
        boxes_being_pushed = set()
        new_pos: Pos = pos[0] + dx, pos[1] + dy
        pos_to_check: set[Pos] = {new_pos}
        while pos_to_check:
            p = pos_to_check.pop()
            if h := hit_box(p):
                boxes_being_pushed.add(h)
                if dy == 0:
                    # horizontal; need to check 2 cells away
                    pos_to_check.add((p[0] + dx * 2, p[1]))
                elif dx == 0:
                    # vertical; need to check 2 cells width
                    pos_to_check.add((h[0], h[1] + dy))
                    pos_to_check.add((h[0] + 1, h[1] + dy))
                else:
                    raise ValueError('Cannot push a box diagonally')
        return boxes_being_pushed

    def advance(pos: Pos, dx: int, dy: int):
        b = boxes_to_push(pos, dx, dy)
        for bx, by in list(b):
            assert (bx, by) in boxes
            boxes.remove((bx, by))
        for bx, by in list(b):
            assert (bx, by) not in walls
            boxes.add((bx + dx, by + dy))
        return pos[0] + dx, pos[1] + dy

    for c, (dx, dy) in [(c, VECTORS[c]) for c in instructions]:
        def dump():
            for y in range(grid.height):
                s = ''
                for x in range(grid.width * 2):
                    if (x, y) == robot_pos:
                        s += c
                    elif (x, y) in boxes:
                        s += '['
                    elif (x - 1, y) in boxes:
                        s += ']'
                    elif (x, y) in walls:
                        s += '#'
                    else:
                        s += '.'
                print(s)
            print('-' * 10)
        if can_advance(robot_pos, dx, dy):
            robot_pos = advance(robot_pos, dx, dy)
        # dump()

    gps_score = sum([x + y * 100 for (x, y) in boxes])
    return gps_score


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
