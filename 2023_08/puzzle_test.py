import math
import re


def test_solve():
    puzzle_input = [
        "RL",
        "",
        "AAA = (BBB, CCC)",
        "BBB = (DDD, EEE)",
        "CCC = (ZZZ, GGG)",
        "DDD = (DDD, DDD)",
        "EEE = (EEE, EEE)",
        "GGG = (GGG, GGG)",
        "ZZZ = (ZZZ, ZZZ)",
    ]
    assert solve(puzzle_input) == 2


def test_solve2():
    puzzle_input = [
        "LR",
        "",
        "11A = (11B, XXX)",
        "11B = (XXX, 11Z)",
        "11Z = (11B, XXX)",
        "22A = (22B, XXX)",
        "22B = (22C, 22C)",
        "22C = (22Z, 22Z)",
        "22Z = (22B, 22B)",
        "XXX = (XXX, XXX)",
    ]
    assert solve2(puzzle_input) == 6


def parse(puzzle_input):
    instruction = list(puzzle_input[0].strip())
    nodes = {}
    for l in puzzle_input[2:]:
        g = re.match(r"(\w+) = \((\w+), (\w+)\)", l).groups()
        n, c = g[0], g[1:]
        nodes[n] = c

    return instruction, nodes


def is_goal(node, problem_part):
    match problem_part:
        case 1:
            return node == "ZZZ"
        case 2:
            return node.endswith('Z')
    raise ValueError()


def get_next_node(node, inst, nodes):
    match inst:
        case "L":
            next_node = nodes[node][0]
        case "R":
            next_node = nodes[node][1]
        case _:
            raise ValueError()
    return next_node

def solve(puzzle_input):
    instruction, nodes = parse(puzzle_input)

    steps = 0
    node = "AAA"
    while True:
        for inst in instruction:
            # print(node)
            next_node = get_next_node(node, inst, nodes)
            steps += 1
            if is_goal(next_node, 1):
                return steps
            node = next_node


def solve2(puzzle_input):
    instruction, nodes = parse(puzzle_input)

    starts = [n for n in nodes.keys() if n.endswith("A")]
    steps_to_z = []
    for n in starts:
        s, _ = steps_to_a_goal(n, instruction, nodes)
        steps_to_z.append(s[0])

    return math.lcm(*steps_to_z)


def steps_to_a_goal(node, instruction, nodes):
    visited = set()
    steps_to_z = []
    steps = 0
    while True:
        for inst in instruction:
            node = get_next_node(node, inst, nodes)
            steps += 1
            mark = node, steps % (len(instruction) * 2)
            if is_goal(node, 2):
                print(f'GOAL {node}')
                steps_to_z.append(steps)
            if mark in visited:
                return steps_to_z, steps
            visited.add(mark)


def test_every_start_goals_in_same_steps_for_every_loop():
    # calculate when it reaches potential goal ('..Z') until it loops back to somewhere already visited
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    instruction, nodes = parse(puzzle_input)

    starts = [n for n in nodes.keys() if n.endswith("A")]
    for n in starts:
        # assert that the steps to reach a goal is same for every loop for each start
        steps_to_z, steps = steps_to_a_goal(n, instruction, nodes)
        assert steps_to_z[-1] % steps_to_z[0] == 0


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
