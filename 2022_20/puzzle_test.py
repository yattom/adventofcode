import pytest


class DList:
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

    @staticmethod
    def generate(puzzle_input):
        l = [DList(None, None, int(v)) for v in puzzle_input]
        for i, e in enumerate(l):
            e.left = l[i - 1]
            e.right = l[(i + 1) % len(l)]
        return l


def move(e):
    v = e.value
    if v > 0:
        while v > 0:
            a = e.left
            b = e
            c = e.right
            d = e.right.right
            a.right = c
            c.left = a
            c.right = b
            b.left = c
            b.right = d
            d.left = b
            v -= 1
    else:
        while v < 0:
            a = e.left.left
            b = e.left
            c = e
            d = e.right
            a.right = c
            c.left = a
            c.right = b
            b.left = c
            b.right = d
            d.left = b
            v += 1


def dump(l):
    # validate(l)
    for e in l:
        if e.value == 0:
            break
    val = []
    for i in range(len(l)):
        val.append(e.value)
        e = e.right
    return val


def validate(l):
    nodes = set()
    lefts = set()
    rights = set()
    for e in l:
        assert e.left.right is e and e.right.left is e
        assert e.left in l and e.right in l
        assert e not in nodes
        nodes.add(e)
        assert e.left not in lefts
        lefts.add(e.left)
        assert e.right not in rights
        rights.add(e.right)
    assert len(l) == len(lefts) == len(rights)


class DList:
    def __init__(self, value, order):
        self.value = value
        self.order = order

    @staticmethod
    def generate(puzzle_input):
        return [DList(int(v), i) for i, v in enumerate(puzzle_input)]


def move(lst, idx):
    idx = idx % len(lst)
    e = lst[idx]
    new_lst = lst[:idx] + lst[idx + 1:]
    new_idx = (idx + e.value) % len(new_lst)
    return new_lst[:new_idx] + [e] + new_lst[new_idx:]


def dump(l):
    for i, e in enumerate(l):
        if e.value == 0:
            zero_idx = i
            break
    lst = []
    for i in range(len(l)):
        lst.append(l[(zero_idx + i) % len(l)].value)
    return lst


def validate(*args):
    pass


def mix(lst):
    for i in range(len(lst)):
        # i == orderになるeのインデックスを得る
        for j, e in enumerate(lst):
            if e.order == i:
                break
        lst = move(lst, j)
        # print(dump(l))
    return lst


def solve(puzzle_input):
    lst = DList.generate(puzzle_input)
    lst = mix(lst)
    vals = dump(lst)
    # print(vals)
    # print(len(vals))
    # print(vals[1000 % len(vals)], vals[2000 % len(vals)], vals[3000 % len(vals)])
    return vals[1000 % len(vals)] + vals[2000 % len(vals)] + vals[3000 % len(vals)]


def solve2(puzzle_input):
    lst = DList.generate(puzzle_input)
    for e in lst:
        e.value *= 811589153
    for i in range(10):
        lst = mix(lst)
    vals = dump(lst)
    return vals[1000 % len(vals)] + vals[2000 % len(vals)] + vals[3000 % len(vals)]


def test_sample1():
    puzzle_input = [
        "1",
        "2",
        "-3",
        "3",
        "-2",
        "0",
        "4",
    ]
    assert solve(puzzle_input) == 3


def test_sample1_strictly():
    puzzle_input = [
        "1",
        "2",
        "-3",
        "3",
        "-2",
        "0",
        "4",
    ]
    dlist = DList.generate([1, 2, -3, 3, -2, 0, 4])
    for i in range(len(dlist)):
        dlist = move(dlist, i)
    assert dump(dlist) == [0, 3, -2, 1, 2, -3, 4]


def test_validate():
    dlist = DList.generate([0, 1, 2, 3, 4, 5])
    validate(dlist)


def test_moving_1():
    dlist = DList.generate([0, 1, 2, 3, 4, 5])
    dlist = move(dlist, 1)
    assert dump(dlist) == [0, 2, 1, 3, 4, 5]


def test_moving_minus1():
    dlist = DList.generate([0, 1, 2, -1, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 1, -1, 2, 4, 5]


def test_moving_to_self():
    dlist = DList.generate([0, 1, 2, -6, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 1, -6, 2, 4, 5]


def test_moving_to_the_left_edge():
    dlist = DList.generate([0, 1, 2, -3, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 1, 2, 4, 5, -3]


def test_moving_to_the_right_edge():
    dlist = DList.generate([0, 1, 2, 2, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 1, 2, 4, 5, 2]


def test_moving_over_the_right_edge():
    dlist = DList.generate([0, 1, 2, 3, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 3, 1, 2, 4, 5]


def test_non_zero_start():
    dlist = DList.generate([4, 5, 0, 1, 2, 3])
    dlist = move(dlist, -1)
    assert dump(dlist) == [0, 3, 1, 2, 4, 5]


def test_moving_over_left_edge():
    dlist = DList.generate([0, 1, 2, -4, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 1, 2, 4, -4, 5]


@pytest.mark.skip
def test_moving_around():
    dlist = DList.generate([1, -2, 3, -4, 5, -6, 7, 0, -8, 9, -20, 21])
    dlist = move(dlist, list(filter(lambda e: e.order == 0, dlist))[0])
    assert dump(dlist) == [0, -8, 9, -20, 21, -2, 1, 3, -4, 5, -6, 7]
    dlist = move(dlist, filter(lambda e: e.order == 0, dlist)[1])
    assert dump(dlist) == [0, -8, 9, -2, -20, 21, 1, 3, -4, 5, -6, 7]
    dlist = move(dlist, filter(lambda e: e.order == 0, dlist)[2])
    assert dump(dlist) == [0, -8, 9, -2, -20, 21, 1, -4, 5, -6, 3, 7]
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, -8, 9, -4, -2, -20, 21, 1, 5, -6, 3, 7]
    dlist = move(dlist, 4)
    assert dump(dlist) == [0, -8, 5, 9, -4, -2, -20, 21, 1, -6, 3, 7]
    dlist = move(dlist, 5)
    assert dump(dlist) == [0, -8, 5, -6, 9, -4, -2, -20, 21, 1, 3, 7]
    dlist = move(dlist, 6)
    assert dump(dlist) == [0, -8, 5, -6, 9, -4, -2, 7, -20, 21, 1, 3]
    dlist = move(dlist, 7)
    assert dump(dlist) == [0, -8, 5, -6, 9, -4, -2, 7, -20, 21, 1, 3]
    dlist = move(dlist, 8)
    assert dump(dlist) == [0, 5, -6, 9, -8, -4, -2, 7, -20, 21, 1, 3]
    dlist = move(dlist, 9)
    assert dump(dlist) == [0, 9, 5, -6, -8, -4, -2, 7, -20, 21, 1, 3]
    dlist = move(dlist, 10)
    assert dump(dlist) == [0, 9, 5, -6, -8, -4, -2, 7, 21, 1, -20, 3]
    dlist = move(dlist, 11)
    assert dump(dlist) == [0, 9, 5, -6, -8, -4, -2, 21, 7, 1, -20, 3]


def test_with_5000_input():
    dlist = DList.generate(list(range(5000)))
    dlist = move(dlist, 10)
    assert dump(dlist)[10] != 10
    assert dump(dlist)[10 + 10] == 10


def test_jumps_over_itself():
    dlist = DList.generate([0, 1, 2, 7, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, 1, 2, 4, 5, 7]


def test_jumps_over_itself_minus():
    dlist = DList.generate([0, 1, 2, -7, 4, 5])
    dlist = move(dlist, 3)
    assert dump(dlist) == [0, -7, 1, 2, 4, 5]


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


def main(solve_puzzle1, solve_puzzle2):
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    solve_puzzle1(puzzle_input)
    solve_puzzle2(puzzle_input)


if __name__ == "__main__":
    main(問題1, 問題2)
