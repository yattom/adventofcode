def puzzle1(lines: list[str]):
    total = 0
    for line in lines:
        vars = line.split()
        value = int(vars[0][:-1])
        nums = [int(v) for v in vars[1:]]

        calcs = [nums[0]]
        for v in nums[1:]:
            new_calcs = []
            for c in calcs:
                new_calcs.append(c + v)
                new_calcs.append(c * v)
            calcs = new_calcs

        if value in calcs:
            total += value

    return total


def puzzle2(lines: list[str]):
    total = 0
    for line in lines:
        vars = line.split()
        value = int(vars[0][:-1])
        nums = [int(v) for v in vars[1:]]

        calcs = [nums[0]]
        for v in nums[1:]:
            new_calcs = []
            for c in calcs:
                new_calcs.append(c + v)
                new_calcs.append(c * v)
                new_calcs.append(int(str(c) + str(v)))
            calcs = new_calcs

        if value in calcs:
            total += value

    return total



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
