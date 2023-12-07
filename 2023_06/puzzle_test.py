import math

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
    p1 = (total_time + math.sqrt(total_time ** 2 - 4 * best_distance)) / 2
    p2 = (total_time - math.sqrt(total_time ** 2 - 4 * best_distance)) / 2
    return abs(math.ceil(min([p1, p2]) + 0.000001) - math.floor(max([p1, p2]) - 0.00001)) + 1


def count_winnable_ways_binary_search(total_time, best_distance):
    def is_win(push_time):
        v = push_time
        run_time = total_time - push_time
        run_distance = v * run_time
        return run_distance > best_distance

    print('@1')
    push_time = 0
    width = total_time // 2
    to_win = [-1, -1]
    while True:
        print(f'{push_time=} {width=}')
        print(f'{is_win(push_time)=} {is_win(push_time + 1)=}')
        if not is_win(push_time) and is_win(push_time + 1):
            to_win[0] = push_time + 1
            break

        width = width // 2
        if width == 0:
            width = 1
        if is_win(push_time):
            push_time -= width
        else:
            push_time += width
        if push_time < 0:
            raise RuntimeError()

    push_time = total_time
    width = total_time // 2
    print('@2')
    while True:
        print(f'{push_time=} {width=}')
        print(f'{is_win(push_time)=} {is_win(push_time + 1)=}')
        if is_win(push_time) and not is_win(push_time + 1):
            to_win[1] = push_time
            break

        width = width // 2
        if width == 0:
            width = 1
        if is_win(push_time):
            push_time += width
        else:
            push_time -= width
        if push_time < 0:
            raise RuntimeError()
    return to_win[1] - to_win[0] + 1


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
