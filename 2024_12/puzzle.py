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


def segregate_areas(grid: Grid) -> list[tuple[str, set[Pos]]]:
    all_cells = [(pos, c) for (pos, c) in grid]
    areas: list[tuple[str, set[Pos]]] = []
    while all_cells:
        start, c = all_cells.pop()
        current_area = set()
        def visit(pos):
            if pos in current_area:
                return
            if (pos, c) in all_cells:
                all_cells.remove((pos, c))
            current_area.add(pos)
            for dx, dy in Grid.NESW:
                new_pos = pos[0] + dx, pos[1] + dy
                if grid[new_pos] == c:
                    visit(new_pos)
        visit(start)
        areas.append((c, current_area))
    return areas


def build_fences(area: set[Pos]) -> set[tuple[float, float]]:
    fences = set()
    for pos in area:
        for dx, dy in Grid.NESW:
            new_pos = pos[0] + dx, pos[1] + dy
            if new_pos not in area:
                fence_pos = pos[0] + dx * 0.1, pos[1] + dy * 0.1
                fences.add(fence_pos)
    return fences


solution = {}

def puzzle1(lines: list[str]):
    grid = parse_as_grid(lines)
    areas = segregate_areas(grid)
    budget = 0
    solution['area_and_fences'] = []
    for _, area in areas:
        area_size = len(area)
        fences = build_fences(area)
        solution['area_and_fences'].append((area, fences))
        budget += area_size * len(fences)
    return budget


def puzzle2(lines: list[str]):
    budget = 0
    for area, fences in solution['area_and_fences']:
        sides = []
        while fences:
            fx, fy = fences.pop()
            side = set()
            sides.append(side)
            def visit(pos, directions):
                if pos in side:
                    return
                side.add(pos)
                if pos in fences:
                    fences.remove(pos)
                for dx, dy in directions:
                    new_pos = pos[0] + dx, pos[1] + dy
                    if new_pos in fences:
                        visit(new_pos, directions)
            if str(fx).endswith('.1') or str(fx).endswith('.9'):
                # going N to S
                visit((fx, fy), [(0, 1), (0, -1)])
            elif str(fy).endswith('.1') or str(fy).endswith('.9'):
                # going E to W
                visit((fx, fy), [(1, 0), (-1, 0)])
            else:
                raise RuntimeError('Unexpected fence position')
        budget += len(area) * len(sides)
    return budget


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
