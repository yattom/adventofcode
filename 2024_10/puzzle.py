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

    def is_point_on_grid(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def find(self, char: str):
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    return x, y
        return None

    def find_all(self, char: str) -> list[tuple[int, int]]:
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c == char:
                    yield x, y

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


NESW = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def puzzle1(lines: list[str]):
    map = parse_as_grid(lines)
    zeros = map.find_all('0')

    score = 0
    for start in zeros:
        height = 0
        steps = {start}
        while height < 9:
            next_steps = set()
            for x, y in steps:
                for dx, dy in NESW:
                    pos = x + dx, y + dy
                    if map[pos] != '' and int(map[pos]) == height + 1:
                        next_steps.add(pos)
            height += 1
            steps = next_steps
        score += len(steps)

    return score


def puzzle2(lines: list[str]):
    map = parse_as_grid(lines)
    zeros = map.find_all('0')

    rating_total = 0
    for start in zeros:
        height = 0
        paths: list[list[tuple[int, int]]] = [[start]]
        while height < 9:
            new_paths = []
            for p in paths:
                x, y = p[-1]
                for dx, dy in NESW:
                    pos = x + dx, y + dy
                    if map[pos] != '' and int(map[pos]) == height + 1:
                        new_paths.append(p + [pos])
            paths = new_paths
            height += 1
        rating_total += len(paths)
    return rating_total

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
