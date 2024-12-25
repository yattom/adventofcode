from puzzle import *

def test_secret_number():
    expected = [
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]
    seed = 123
    for e in expected:
        assert secret_number(seed) == e
        seed = e