from dataclasses import dataclass
import pytest


@pytest.fixture
def puzzle_input():
    return [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]


def test_solve(puzzle_input):
    assert solve(puzzle_input) == 35


def test_solve2(puzzle_input):
    assert solve2(puzzle_input) == 46


def test_parse(puzzle_input):
    seeds, maps = parse(puzzle_input)
    assert seeds == [79, 14, 55, 13]
    assert len(maps) == 7


def parse(puzzle_input):
    seeds = [int(s) for s in puzzle_input[0].split()[1:]]
    maps = []
    for l in puzzle_input[2:]:
        if not l:
            continue
        if 'map:' in l:
            title = l.split()[0].split('-')
            maps.append(ResourceMap(title=title))
        else:
            dst_start, src_start, length = [int(s) for s in l.split()]
            maps[-1].add_mapping(dst_start, src_start, length)

    return seeds, maps


class ResourceMap:
    def __init__(self, title):
        self.title = title
        self.mappings: list[tuple[Range, Range]] = []

    def add_mapping(self, dst_start, src_start, length):
        self.mappings.append((Range(dst_start, length), Range(src_start, length)))

    def dst(self, src):
        for dst_rng, src_rng in self.mappings:
            if src_rng.start <= src < src_rng.start + src_rng.length:
                return dst_rng.start + src - src_rng.start
        return src

    def dst_range(self, other: 'Range | CombinedRange'):
        if isinstance(other, Range):
            inner = other
            other = CombinedRange()
            other.combine(inner)
        mapped_rng = CombinedRange()
        r: Range
        for r in other.ranges:
            for dst_rng, src_rng in self.mappings:
                if src_rng.has_intersection(r):
                    print(f'@1 {dst_rng=} {src_rng=} {r=}')
                    s = src_rng.intersection(r)
                    d = Range(dst_rng.start + s.start - src_rng.start, s.length)
                    mapped_rng.combine(d)
                    r = r.difference(s)
                    print(f'@2 {d=} {s=} {r=}')
                if r.is_empty():
                    break
            else:
                mapped_rng.combine(r)

        return mapped_rng


def test_combined_range_has_interstction():
    r1 = Range(1, 5)
    r2 = Range(3, 9)
    assert r1.has_intersection(r2)


def test_combined_range_combination():
    r1 = Range(1, 4)
    r2 = Range(3, 9)
    r1_2 = r1.intersection(r2)
    r3 = Range(6, 1)
    r4 = Range(8, 2)
    r3_4 = r3.combine(r4)
    cmb = r1_2.combine(r3_4)
    assert list(cmb.enumerate()) == [3, 4, 6, 8, 9]


@pytest.mark.parametrize(
    'src, expected_dst',
    [
        ((0, 10), [(30, 10)]),
        ((25, 10), [(15, 5), (30, 5)]),
        ((5, 10), [(35, 5), (10, 5)]),
    ]
)
def test_mapping_range(src, expected_dst):
    # Arrange
    # build simple ResourceMap with 2 distinguished ranges
    # 1. 0-9 -> 30-39
    # 2. 20-29 -> 10-19
    rmap = ResourceMap(title=['a', 'b'])
    rmap.add_mapping(30, 0, 10)
    rmap.add_mapping(10, 20, 10)

    # Act

    # Assert
    # check the result
    expected = CombinedRange()
    for e in expected_dst:
        expected.combine(Range(*e))
    assert rmap.dst_range(Range(*src)) == expected


@dataclass
class Range:
    start: int
    length: int

    def __contains__(self, item):
        return self.start <= item < self.start + self.length

    def intersection(self, other):
        if not self.has_intersection(other):
            raise ValueError("No intersection")
        start = max(self.start, other.start)
        end = min(self.start + self.length, other.start + other.length)
        return Range(start, end - start)

    def has_intersection(self, other):
        if isinstance(other, CombinedRange):
            return other.has_intersection(self)
        start = max(self.start, other.start)
        end = min(self.start + self.length, other.start + other.length)
        return start <= end

    def combine(self, other):
        if not self.has_intersection(other):
            cmb = CombinedRange()
            cmb.combine(self)
            cmb.combine(other)
            return cmb
        start = min(self.start, other.start)
        end = max(self.start + self.length, other.start + other.length)
        return Range(start, end - start)

    def enumerate(self):
        return range(self.start, self.start + self.length)

    def __lt__(self, other):
        return self.start < other.start

    def difference(self, other):
        if not self.has_intersection(other):
            return self
        if self.start < other.start:
            return Range(self.start, other.start - self.start)
        else:
            return Range(other.start + other.length, self.start + self.length - other.start - other.length)

    def is_empty(self):
        return self.length == 0


class CombinedRange:
    def __init__(self):
        self.ranges = []

    def has_intersection(self, other):
        pass

    def combine(self, other):
        if isinstance(other, CombinedRange):
            for r in other.ranges:
                self.combine(r)
            return
        for i, r in enumerate(self.ranges):
            if r.has_intersection(other):
                self.ranges[i] = r.combine(other)
                return
        else:
            self.ranges.append(other)

    def enumerate(self):
        for r in self.ranges:
            yield from r.enumerate()

    def __repr__(self):
        return f"CombinedRange({self.ranges})"

    def __eq__(self, other):
        if not isinstance(other, CombinedRange):
            return False
        return self.ranges == other.ranges


def solve(puzzle_input):
    seeds, maps = parse(puzzle_input)
    locations = []
    for s in seeds:
        for m in maps:
            s = m.dst(s)
        locations.append(s)
    return min(locations)


def solve2(puzzle_input):
    seeds, maps = parse(puzzle_input)
    actual_seeds = [Range(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    locations: list[CombinedRange] = []
    for r in actual_seeds:
        for m in maps:
            r = m.dst_range(r)
        locations.append(r)
    return min([min([r.start for r in l.ranges]) for l in locations])


def 問題1(puzzle_input: list[str]):
    print(solve(puzzle_input))


def 問題2(puzzle_input: list[str]):
    print(solve2(puzzle_input))


if __name__ == "__main__":
    with open("puzzle_input.txt") as f:
        puzzle_input = f.read().splitlines()
    問題1(puzzle_input)
    問題2(puzzle_input)
