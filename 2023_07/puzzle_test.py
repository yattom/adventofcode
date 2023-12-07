TYPES = {
    (5,): ("FIVE_OF_A_KIND", 6),
    (4, 1): ("FOUR_OF_A_KIND", 5),
    (3, 2): ("FULL_HOUSE", 4),
    (3, 1, 1): ("THREE_OF_A_KIND", 3),
    (2, 2, 1): ("TWO_PAIR", 2),
    (2, 1, 1, 1): ("ONE_PAIR", 1),
    (1, 1, 1, 1, 1): ("HIGH_CARD", 0),

}


def test_solve():
    puzzle_input = [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]
    assert solve(puzzle_input) == 6440


def test_solve2():
    puzzle_input = [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]
    assert solve2(puzzle_input) == 5905


def test_solve2_J_is_wak():
    puzzle_input = [
        "J2222 1",
        "2222J 3",
    ]
    assert solve2(puzzle_input) == 3 * 2 + 1
    assert solve(puzzle_input) == 1 * 2 + 3


def test_split_str():
    assert list('ABC') == ['A', 'B', 'C']


def test_decide_hand_type():
    assert decide_hand_type('33333')[0] == "FIVE_OF_A_KIND"
    assert decide_hand_type('KTJJT')[0] == "TWO_PAIR"


def decide_hand_type(hand, joker=False):
    hand = sorted(list(hand))
    sames = []
    jokers = 0
    for i, c in enumerate(hand):
        if joker and c == 'J':
            jokers += 1
            continue
        if i == 0:
            sames.append(1)
        elif c == hand[i - 1]:
            sames[-1] += 1
        else:
            sames.append(1)
    if joker:
        if len(sames) == 0:
            sames = [5]
        else:
            sames = sorted(sames, reverse=True)
            sames[0] += jokers
    return TYPES[tuple(sorted(sames, reverse=True))]


def solver(puzzle_input, order, joker):
    # evals is a list of hands to sort by 1. hand_type, 2. each card in hand in specified order
    evals: list[tuple[int, list[int], int]] = []
    for l in puzzle_input:
        hand, bid = l.split()
        _, hand_type = decide_hand_type(hand, joker)
        bid = int(bid)
        evals.append((hand_type, [-order.index(c) for c in hand], bid))
    evals.sort(reverse=False)
    score = 0
    for i, (hand_type, hand, bid) in enumerate(evals):
        score += bid * (i + 1)
    return score


def solve(puzzle_input):
    ORDER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    return solver(puzzle_input, ORDER, False)


def solve2(puzzle_input):
    ORDER = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    return solver(puzzle_input, ORDER, True)


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
