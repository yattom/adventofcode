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
Heading: TypeAlias = int


class DynamicPlanningTable:
    AVAILABLE = 1

    @dataclass
    class Passage:
        score: int
        before: set[(Pos, Heading)]

        def __init__(self, score: int):
            self.score = score
            self.before = set()

    def __init__(self):
        self.score_list = []
        self.passage_map: dict[tuple[Pos, Heading], DynamicPlanningTable.Passage] = {}
        pass

    def store(self, score: int, pos: Pos, heading: Heading, before: tuple[Pos, Heading] | None):
        while len(self.score_list) <= score:
            self.score_list.append({})
        self.score_list[score][(pos, heading)] = DynamicPlanningTable.AVAILABLE
        if (pos, heading) not in self.passage_map:
            self.passage_map[(pos, heading)] = DynamicPlanningTable.Passage(score)
        if before:
            before_pos, before_heading = before
            self.passage_map[(pos, heading)].before.add((before_pos, before_heading))

    def get_for_score(self, score) -> list[tuple[Pos, Heading]]:
        if score < 0 or len(self.score_list) <= score:
            return []
        return self.score_list[score].keys()

    def already_available(self, pos: Pos, heading: Heading, score: int) -> bool:
        if (p := (pos, heading)) in self.passage_map:
            return self.passage_map[p].score < score
        return False

PUZZLE1_ANSWER = []

def puzzle1(lines: list[str]):
    maze = parse_as_grid(lines)
    start = maze.find('S')
    end = maze.find('E')
    passable = list(maze.find_all('.')) + [start, end]

    score = 0
    dp_table = DynamicPlanningTable()
    dp_table.store(score, start, 1, before=None)
    while True:
        if any([pos == end for (pos, _) in dp_table.get_for_score(score)]):
            break
        score += 1
        any_changes = False
        for pos, heading in dp_table.get_for_score(score - 1):
            dx, dy = NESW[heading]
            p = pos[0] + dx, pos[1] + dy
            if p in passable:
                if not dp_table.already_available(p, heading, score):
                    dp_table.store(score, p, heading, before=(pos, heading))
                    any_changes = True
        for pos, heading in dp_table.get_for_score(score - 1000):
            h1 = (heading - 1) % len(NESW)
            h2 = (heading + 1) % len(NESW)
            if not dp_table.already_available(pos, h1, score):
                dp_table.store(score, pos, h1, before=(pos, heading))
                any_changes = True
            if not dp_table.already_available(pos, h2, score):
                dp_table.store(score, pos, h2, before=(pos, heading))
                any_changes = True

        if any_changes:
            print(f'{score=}')
            # maze.dump({pos: '^>v<'[heading] for pos, heading in dp_table.get_for_score(score)})
            # print(dp_table.get_for_score(score))

    PUZZLE1_ANSWER.append(end)
    PUZZLE1_ANSWER.append(dp_table)
    PUZZLE1_ANSWER.append(maze)
    return score


def puzzle2(lines: list[str]):
    end = PUZZLE1_ANSWER[0]
    dp_table = PUZZLE1_ANSWER[1]
    maze = PUZZLE1_ANSWER[2]
    states = [x for x in dp_table.passage_map.keys() if x[0] == end]

    tiles: set[Pos] = set()
    while states:
        pos, heading = states.pop()
        tiles.add(pos)
        if dp_table.passage_map[(pos, heading)].before:
            states += list(dp_table.passage_map[(pos, heading)].before)

    maze.dump({pos: 'O' for pos in tiles})
    return len(tiles)


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
