import time
from dataclasses import dataclass
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


NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def puzzle1(lines: list[str]):
    maze = parse_as_grid(lines)
    path, reverse_path = find_path(maze)

    cheats = find_cheats(maze, path, reverse_path, distance=2)
    return cheats


def find_path(maze):
    start = maze.find('S')
    end = maze.find('E')
    pos = start
    steps = 0
    path: list[Pos] = [start]
    reverse_path: dict[Pos, int] = {start: steps}
    while pos != end:
        next_points = [(dx, dy) for (dx, dy) in NESW if maze[pos[0] + dx, pos[1] + dy] in '.SE']
        assert ((pos == start or pos == end) and len(next_points) == 1 or len(next_points) == 2)
        for dx, dy in NESW:
            p = pos[0] + dx, pos[1] + dy
            if maze[p] in '.E' and p not in reverse_path:
                pos = p
                break
        else:
            raise RuntimeError('No path found', pos)

        steps += 1
        path.append(pos)
        reverse_path[pos] = steps
    return path, reverse_path


def cheat_distance(maze, start_pos, end_pos, distance_cap) -> int | None:
    return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])

    start_ok = False
    end_ok = False
    if end_pos[0] - start_pos[0] > 0:
        # end is to the East; it's good to have a wall at E of start
        if maze[start_pos[0] + 1, start_pos[1]] == '#':
            start_ok = True
        # ... and it's also good to have a wall at W of end
        if maze[end_pos[0] - 1, end_pos[1]] == '#':
            end_ok = True
    if end_pos[0] - start_pos[0] < 0:
        # end is to the West; it's good to have a wall at W of start
        if maze[start_pos[0] - 1, start_pos[1]] == '#':
            start_ok = True
        # ... and it's also good to have a wall at E of end
        if maze[end_pos[0] + 1, end_pos[1]] == '#':
            end_ok = True
    if end_pos[1] - start_pos[1] > 0:
        # end is to the South; it's good to have a wall at S of start
        if maze[start_pos[0], start_pos[1] + 1] == '#':
            start_ok = True
        # ... and it's also good to have a wall at N of end
        if maze[end_pos[0], end_pos[1] - 1] == '#':
            end_ok = True
    if end_pos[1] - start_pos[1] < 0:
        # end is to the North; it's good to have a wall at N of start
        if maze[start_pos[0], start_pos[1] - 1] == '#':
            start_ok = True
        # ... and it's also good to have a wall at S of end
        if maze[end_pos[0], end_pos[1] + 1] == '#':
            end_ok = True

    if start_ok and end_ok:
        return abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1])
    else:
        return None



def puzzle2(lines: list[str]):
    maze = parse_as_grid(lines)
    path, reverse_path = find_path(maze)

    cheats = find_cheats(maze, path, reverse_path, distance=20)
    return cheats


def find_cheats(maze, path, reverse_path, distance):
    sampling = {}
    cheats = 0
    for pos in path:
        for p in path:
            if (d := (abs(p[0] - pos[0]) + abs(p[1] - pos[1]))) <= distance:
                cd = cheat_distance(maze, pos, p, d)
                effect = reverse_path[pos] - reverse_path[p] - d
                if cd is None:
                    continue
                if effect >= 0:
                    sampling[effect] = sampling.get(effect, 0) + 1
                if effect >= 100:
                    cheats += 1
    print(sampling)
    return cheats


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
