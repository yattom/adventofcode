import re


def test_solve2():
    puzzle_input = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]
    assert solve2(puzzle_input) == 281

def solve(puzzle_input):
    total = 0
    for l in puzzle_input:
        nums = re.findall(r'\d', l)
        num = int(nums[0]) * 10 + int(nums[-1])
        total += num
    return total


NUMS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def solve2(puzzle_input):
    total = 0
    for l in puzzle_input:
        nums = []
        for i in range(0, len(l)):
            for w in NUMS:
                if l[i:].startswith(w):
                    nums.append(w)
                    break
        n1 = NUMS[nums[0]]
        n2 = NUMS[nums[-1]]
        num = n1 * 10 + n2
        # print(l, nums, n1, n2, num)
        total += num
    return total


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
