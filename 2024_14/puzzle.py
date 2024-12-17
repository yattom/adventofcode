import re
from functools import reduce


def parse(lines: list[str]):
    for l in lines:
        g = re.search(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', l).groups()
        p = (int(g[0]), int(g[1]))
        v = (int(g[2]), int(g[3]))
        yield p, v


ROOM_SIZE = (101, 103)


def calc_position(p, v, after, room_size=ROOM_SIZE):
    new_pos = ((p[0] + v[0] * after) % room_size[0],
               (p[1] + v[1] * after) % room_size[1])
    return new_pos


def puzzle1(lines: list[str]):
    qnum = [0, 0, 0, 0]
    for p, v in parse(lines):
        final_pos = calc_position(p, v, after=100)

        if final_pos[0] < int(ROOM_SIZE[0] / 2) and final_pos[1] < int(ROOM_SIZE[1] / 2):
            qnum[0] += 1
        elif final_pos[0] > int(ROOM_SIZE[0] / 2) and final_pos[1] < int(ROOM_SIZE[1] / 2):
            qnum[1] += 1
        elif final_pos[0] < int(ROOM_SIZE[0] / 2) and final_pos[1] > int(ROOM_SIZE[1] / 2):
            qnum[2] += 1
        elif final_pos[0] > int(ROOM_SIZE[0] / 2) and final_pos[1] > int(ROOM_SIZE[1] / 2):
            qnum[3] += 1

    return reduce(lambda x, y: x * y, qnum, 1)


def calc_score(positions, cap):
    score = 0
    box = 3
    for y in range(0, ROOM_SIZE[1], box):
        for x in range(0, ROOM_SIZE[0], box):
            count = sum([1 for i in range(box) for j in range(box) if (x + i, y + j) in positions])
            if count > 3:
                score += 1
    return score



def puzzle2(lines: list[str]):
    robots = [(p, v) for p, v in parse(lines)]
    max_score = 0
    for i in range(10000):
        positions = set([calc_position(p, v, after=i) for p, v in robots])
        score = calc_score(positions, 3)
        if score > max_score:
            max_score = score
            dump_robots(i, positions)


def dump_robots(i, positions):
    print(f'After {i} seconds:')
    for y in range(ROOM_SIZE[1]):
        l = []
        for x in range(ROOM_SIZE[0]):
            if (x, y) in positions:
                l.append('#')
            else:
                l.append('.')
        print(''.join(l))
    print('=' * ROOM_SIZE[0])


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
