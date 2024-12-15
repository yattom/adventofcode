def puzzle1(lines: list[str]):
    stones = [int(v) for v in lines[0].strip().split()]

    new_stones = 0
    for s in stones:
        new_stones += stones_after_blinks(s, 25)

    return new_stones


known_results: dict[tuple[int, int], int] = {}

def stones_after_blinks(initial: int, n: int) -> int:
    if n == 0:
        return 1
    if (initial, n) in known_results:
        return known_results[(initial, n)]
    stones = [initial]
    new_stones = []
    for s in stones:
        match s:
            case 0:
                new_stones = stones_after_blinks(1, n - 1)
            case _ if len(str(s)) % 2 == 0:
                s1, s2 = str(s)[:len(str(s)) // 2], str(s)[len(str(s)) // 2:]
                new_stones = stones_after_blinks(int(s1), n - 1) + stones_after_blinks(int(s2), n - 1)
            case _:
                new_stones = stones_after_blinks(s * 2024, n - 1)
    known_results[(initial, n)] = new_stones
    return new_stones

def puzzle2(lines: list[str]):
    stones = [int(v) for v in lines[0].strip().split()]

    new_stones = 0
    for s in stones:
        new_stones += stones_after_blinks(s, 75)

    return new_stones



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
