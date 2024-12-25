from puzzle import *


def test_all_combination_of_pairs():
    assert sorted(list(all_combination_of_pairs(2, (1, 4)))) == [
        [(1, 2), (3, 4)], [(1, 3), (2, 4)], [(1, 4), (2, 3)]]
    assert sorted(list(all_combination_of_pairs(4, (1, 4)))) == sorted([
    ])
