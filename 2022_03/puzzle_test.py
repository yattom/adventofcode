P = {c: ord(c) - ord('a') + 1 for c in "abcdefghijklmnopqrstuvwxyz"}
P.update({c: ord(c) - ord('A') + 27 for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"})


def solve(puzzle_input):
    score = 0
    for rucksack in puzzle_input:
        compartments = [set(), set()]
        duplicate = None
        if len(rucksack) % 2 != 0:
            raise ValueError(f"Rucksack {rucksack} has odd number of items")
        for i in range(int(len(rucksack) / 2)):
            if rucksack[i] not in compartments[1]:
                compartments[0].add(rucksack[i])
            else:
                duplicate = rucksack[i]
                break
            if rucksack[-i - 1] not in compartments[0]:
                compartments[1].add(rucksack[-i - 1])
            else:
                duplicate = rucksack[-i - 1]
                break
        else:
            raise ValueError(f"No duplicate found in rucksack {rucksack}")
        score += P[duplicate]
    return score


def solve2(puzzle_input):
    score = 0
    for l in range(0, len(puzzle_input), 3):
        i1, i2, i3 = set(puzzle_input[l]), set(puzzle_input[l + 1]), set(puzzle_input[l + 2])
        s = i1.intersection(i2).intersection(i3).pop()
        score += P[s]
    return score



def test_sample():
    puzzle_input = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert solve(puzzle_input) == 157


def test_sample2():
    puzzle_input = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert solve2(puzzle_input) == 70


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
