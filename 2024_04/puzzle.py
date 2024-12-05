def count_word(line: str, word: str):
    return line.count(word)


def reverse_horizontal(line: str):
    return line[::-1]


def vertical_lines(lines: list[str]) -> list[str]:
    for x in range(len(lines[0])):
        yield ''.join([line[x] for line in lines])


def diagonal_rightside_down_lines(lines: list[str]) -> list[str]:
    max_x = len(lines[0])
    max_y = len(lines)
    for x in range(max_x - 1, -1, -1):
        yield ''.join([lines[xx - x][xx] for xx in range(x, max_x) if (xx - x) < max_y])
    for y in range(1, max_y):
        yield ''.join([lines[yy][yy - y] for yy in range(y, max_y) if (yy - y) < max_x])


def test_diagonal_rightside_down_lines_height_is_smaller_than_width():
    lines = ['123456789'] * 5
    assert list(diagonal_rightside_down_lines(lines)) == [
        '9', '89', '789', '6789', '56789', '45678', '34567', '23456', '12345',
        '1234', '123', '12', '1',
    ]


def test_diagonal_rightside_down_lines_correct_order():
    lines = ['123456789', 'abcdefghi', 'ABCDEFGHI']
    assert list(diagonal_rightside_down_lines(lines)) == [
        '9', '8i', '7hI', '6gH', '5fG', '4eF', '3dE', '2cD', '1bC',
        'aB', 'A'
    ]


WORD = 'XMAS'


def puzzle1(lines: list[str]):
    total = 0
    for line in lines:
        total += count_word(line, WORD) + count_word(reverse_horizontal(line), WORD)
    for line in vertical_lines(lines):
        total += count_word(line, WORD) + count_word(reverse_horizontal(line), WORD)
    for line in diagonal_rightside_down_lines(lines):
        total += count_word(line, WORD) + count_word(reverse_horizontal(line), WORD)
    for line in diagonal_rightside_down_lines([reverse_horizontal(l) for l in lines]):
        total += count_word(line, WORD) + count_word(reverse_horizontal(line), WORD)
    return total


def puzzle2(lines: list[str]):
    MS_AND_SS = ['MMSS', 'SMSM', 'SSMM', 'MSMS']
    max_x = len(lines[0])
    max_y = len(lines)
    count = 0
    for x in range(max_x - 2):
        for y in range(max_y - 2):
            center = lines[y + 1][x + 1]
            hands = lines[y][x] + lines[y][x + 2] + lines[y + 2][x] + lines[y + 2][x + 2]
            if center == 'A' and hands in MS_AND_SS:
                count += 1
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
