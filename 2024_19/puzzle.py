from dataclasses import dataclass, field


@dataclass
class VisitedEntry:
    working: str
    prev_working: list[str] = field(default_factory=list)


class Paths:
    def __init__(self):
        self.paths = {}

    def add(self, working: str, prev_working: str):
        if working not in self.paths:
            self.paths[working] = []
        self.paths[working].append(prev_working)

    def get_prev_working(self, working: str) -> list[str]:
        return self.paths.get(working, [])

    def __repr__(self):
        return repr(self.paths)


def make_towel(pattern: str, towels: list[str], working: str, prev_working: str, visited: set[str],
               paths: Paths, selections: list[int] = None) -> bool:
    if not selections:
        selections = []
    paths.add(working, prev_working)
    if working in visited:
        return False
    visited.add(working)
    if pattern == working:
        return True
    # print(f'{pattern=}   {working=}  {selections=}')
    found = False
    for i, t in enumerate(towels):
        # print(f'{working=} {t=}')
        if len(working) + len(t) > len(pattern):
            continue
        if pattern.startswith(working + t):
            result = make_towel(pattern, towels, working + t, working, visited, paths, selections + [i])
            if result:
                found = True
    return found


def puzzle1(lines: list[str]):
    towels = [s.strip() for s in lines[0].strip().split(',')]
    patterns = [l.strip() for l in lines[2:]]

    count = 0
    for p in patterns:
        if make_towel(p, towels, "", '', set(), Paths()):
            count += 1

    return count


def puzzle2(lines: list[str]):
    towels = [s.strip() for s in lines[0].strip().split(',')]
    patterns = [l.strip() for l in lines[2:]]

    count = 0
    for p in patterns:
        if make_towel(p, towels, "", '', set(), paths := Paths()):
            memo = {}

            def count_paths(working):
                # print(f'{working}')
                if working in memo:
                    return memo[working]
                total = 0
                for p in paths.get_prev_working(working):
                    if p == '':
                        total += 1
                    else:
                        total += count_paths(p)
                memo[working] = total
                return total

            path_count = count_paths(p)
            # print(f'{path_count=} {paths=} {memo=}')

            count += path_count

    return count


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
