from copy import copy


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

    def find(self, char: str):
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    return x, y
        return None

    def dump(self, marks: dict[tuple[int, int], str] = None):
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


def parse_as_grid(lines: list[str]):
    return Grid([list(line.strip()) for line in lines])


class Vector:
    VECTORS = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0),
    }

    def __init__(self, heading: str = 'N'):
        self.x, self.y = self.VECTORS[heading]

    def turn_left(self) -> 'Vector':
        v = Vector()
        v.x, v.y = self.y, -self.x
        return v

    def turn_right(self) -> 'Vector':
        v = Vector()
        v.x, v.y = -self.y, self.x
        return v

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def puzzle1(lines: list[str]):
    grid = parse_as_grid(lines)
    start = grid.find('^')
    heading = Vector()

    path = plan_path(grid, heading, start)
    # grid.dump({pos: 'X' for pos in path})
    return len(path)


def plan_path(grid, heading, start):
    x, y = start
    path: set[tuple[int, int]] = set()
    while True:
        if not (0 <= x < grid.width and 0 <= y < grid.height):
            break
        path.add((x, y))
        if grid[x + heading.x, y + heading.y] == '#':
            heading = heading.turn_right()
        else:
            x, y = x + heading.x, y + heading.y
    return path


def detect_loop(start: tuple[int, int], heading: Vector, grid: Grid) -> bool:
    turns: set[tuple[int, int, Vector]] = set()
    x, y = start
    path: set[tuple[int, int]] = set()
    while True:
        if not (0 <= x < grid.width and 0 <= y < grid.height):
            return False
        path.add((x, y))
        if grid[x + heading.x, y + heading.y] == '#':
            if (x, y, heading) in turns:
                # p = {pos: 'X' for pos in path}
                # p.update({pos: '*' for pos in turns})
                # grid.dump(p)
                return True
            turns.add((x, y, heading))
            heading = heading.turn_right()
        else:
            x, y = x + heading.x, y + heading.y


def puzzle2(lines: list[str]):
    grid = parse_as_grid(lines)
    start = grid.find('^')
    path = plan_path(grid, Vector(), start) - {start}
    obstacles = set()
    for pos in list(path):
    # for pos in [(x, y) for x in range(grid.width) for y in range(grid.height)]:
        new_grid = copy(grid)
        new_grid[pos] = '#'
        if detect_loop(start, Vector(), new_grid):
            obstacles.add(pos)
    return len(obstacles - {start})


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
