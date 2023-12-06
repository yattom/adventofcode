def test_solve():
    puzzle_input = [
        "Time:      7  15   30",
        "Distance:  9  40  200",
    ]
    assert solve(puzzle_input) == 288


def test_solve2():
    puzzle_input = [
        "Time:      7  15   30",
        "Distance:  9  40  200",
    ]
    assert solve2(puzzle_input) == 71503


def count_winnable_ways(total_time, best_distance):
    tally = 0
    for push_time in range(0, total_time + 1):
        v = push_time
        run_time = total_time - push_time
        run_distance = v * run_time
        if run_distance > best_distance:
            tally += 1
    return tally


def solve(puzzle_input):
    times = [int(s) for s in puzzle_input[0].split()[1:]]
    distances = [int(s) for s in puzzle_input[1].split()[1:]]

    final_score = 1
    for i in range(len(times)):
        total_time, best_distance = times[i], distances[i]
        final_score *= count_winnable_ways(total_time, best_distance)
    return final_score


def solve2(puzzle_input):
    total_time = int(''.join(puzzle_input[0].split()[1:]))
    best_distance = int(''.join(puzzle_input[1].split()[1:]))

    return count_winnable_ways(total_time, best_distance)



def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
