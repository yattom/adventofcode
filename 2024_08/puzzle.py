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


def puzzle1(lines: list[str]):
    grid = parse_as_grid(lines)

    antennas: dict[str, list[tuple[int, int]]] = {}
    for y, row in enumerate(grid.grid):
        for x, c in enumerate(row):
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((x, y))

    antinodes: set[tuple[int, int]] = set()
    for pos_list in antennas.values():
        for i, (x1, y1) in enumerate(pos_list):
            for (x2, y2) in pos_list[i + 1:]:
                dx = x2 - x1
                dy = y2 - y1
                nx1, ny1 = x1 - dx, y1 - dy
                nx2, ny2 = x2 + dx, y2 + dy
                if grid.is_point_on_grid((nx1, ny1)):
                    antinodes.add((nx1, ny1))
                if grid.is_point_on_grid((nx2, ny2)):
                    antinodes.add((nx2, ny2))

    grid.dump({pos: '#' for pos in antinodes})
    return len(antinodes)

def puzzle2(lines: list[str]):
    grid = parse_as_grid(lines)

    antennas: dict[str, list[tuple[int, int]]] = {}
    for y, row in enumerate(grid.grid):
        for x, c in enumerate(row):
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((x, y))

    antinodes: set[tuple[int, int]] = set()
    for pos_list in antennas.values():
        for i, (x1, y1) in enumerate(pos_list):
            for (x2, y2) in pos_list[i + 1:]:
                dx = x2 - x1
                dy = y2 - y1
                for i in range(0, 9999999999):
                    nx, ny = x1 - dx * i, y1 - dy * i
                    if grid.is_point_on_grid((nx, ny)):
                        antinodes.add((nx, ny))
                    else:
                        break
                for i in range(-1, -9999999999, -1):
                    nx, ny = x1 - dx * i, y1 - dy * i
                    if grid.is_point_on_grid((nx, ny)):
                        antinodes.add((nx, ny))
                    else:
                        break

    grid.dump({pos: '#' for pos in antinodes})
    return len(antinodes)

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
