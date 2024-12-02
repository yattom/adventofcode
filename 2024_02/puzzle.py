def direction(v1, v2):
    if v1 < v2:
        return 1
    elif v1 > v2:
        return -1
    else:
        return 0

def is_safe(nums: list[int]):
    if len(nums) == 1:
        return True
    d = direction(nums[0], nums[1])
    if d == 0:
        return False
    for i in range(0, len(nums) - 1):
        if abs(nums[i + 1] - nums[i]) > 3:
            return False
        if d != direction(nums[i], nums[i + 1]):
            return False
    return True


def puzzle1(lines: list[str]):
    safe_report_count = 0
    for line in lines:
        nums = [int(v) for v in line.split()]
        if is_safe(nums):
            safe_report_count += 1
    return safe_report_count


def puzzle2(lines: list[str]):
    safe_report_count = 0
    for line in lines:
        nums = [int(v) for v in line.split()]
        for i in range(len(nums)):
            if is_safe(nums[:i] + nums[i + 1:]):
                safe_report_count += 1
                break
    return safe_report_count



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