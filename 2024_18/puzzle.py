from typing import TypeAlias

Pos: TypeAlias = tuple[int, int]
NESW = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def dump(maze: dict[Pos, bool], marks: dict[Pos, str] = {}):
    min_x = min(x for x, y in maze)
    max_x = max(x for x, y in maze)
    min_y = min(y for x, y in maze)
    max_y = max(y for x, y in maze)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in marks:
                print(marks[(x, y)], end='')
            else:
                print('#' if maze.get((x, y), False) else '.', end='')
        print()
    print()


def solve(maze: dict[Pos, bool], maze_size: Pos):
    start = (0, 0)
    goal = (maze_size[0] - 1, maze_size[1] - 1)

    visited: set[Pos] = set()
    next_steps = [start]
    step_count = 0
    while True:
        if not next_steps:
            return -1
        next_next_steps = set()
        for x, y in next_steps:
            if (x, y) == goal:
                return step_count
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in NESW:
                if not (0 <= x + dx < maze_size[0] and 0 <= y + dy < maze_size[1]):
                    continue
                if not (x + dx, y + dy) in maze:
                    next_next_steps.add((x + dx, y + dy))
        next_steps = next_next_steps
        step_count += 1
        # dump(maze, marks={p: 'O' for p in visited})

def puzzle1(lines: list[str]):
    maze_size = 71, 71
    maze: dict[Pos, bool] = {}
    for i in range(1024):
        if len(lines) <= i:
            break
        x, y = [int(x) for x in lines[i].strip().split(',')]
        maze[(x, y)] = True
    # dump(maze)

    return solve(maze, maze_size)




def puzzle2(lines: list[str]):
    maze_size = 71, 71
    maze: dict[Pos, bool] = {}
    for l in lines:
        x, y = [int(x) for x in l.strip().split(',')]
        maze[(x, y)] = True
        steps = solve(maze, maze_size)
        # print(f'{x=}, {y=}, {steps=}')
        if steps < 0:
            return x, y
    return None


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
