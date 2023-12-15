def test_solve():
    puzzle_input = [
        "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot",
        "=9,ab=5,pc-,pc=6,ot=7"
    ]
    assert solve(puzzle_input) == 1320


def test_solve2():
    puzzle_input = [
        "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot",
        "=9,ab=5,pc-,pc=6,ot=7"
    ]
    assert solve2(puzzle_input) == 145


def solve(puzzle_input):
    line = "".join(puzzle_input)
    tally = 0
    for s in line.split(","):
        tally += my_hash(s)

    return tally


def my_hash(s):
    val = 0
    for c in s:
        n = ord(c)
        val += n
        val *= 17
        val = val % 256
    return val


def solve2(puzzle_input):
    line = "".join(puzzle_input)
    tally = 0
    boxes: list[list[list[str]]] = [list() for i in range(256)]
    for s in line.split(","):
        # for i, b in enumerate(boxes):
        #     if b:
        #         print(f"box[{i}] = {b}")
        if '-' in s:
            label = s.split('-')
            h = my_hash(label[0])
            for i, l in enumerate(boxes[h]):
                if l[0] == label[0]:
                    boxes[h] = boxes[h][:i] + boxes[h][i+1:]
                    break
        elif '=' in s:
            label = s.split('=')
            h = my_hash(label[0])
            for i, l in enumerate(boxes[h]):
                if l[0] == label[0]:
                    boxes[h][i] = label
                    break
            else:
                boxes[h].append(label)

    power = 0
    for i, b in enumerate(boxes):
        for j, l in enumerate(b):
            p = (i + 1) * (j + 1) * int(l[1])
            power += p
    return power




def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)