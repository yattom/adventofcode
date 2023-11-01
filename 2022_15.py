import re
import os
from dataclasses import dataclass


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

@dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int

    def distance(self):
        return distance(self.x, self.y, self.beacon_x, self.beacon_y)

    def cover_area(self):
        d = self.distance()
        return Area(self.x - d, self.y - d, self.x + d, self.y + d)

    def get_row(self, y):
        d = self.distance() - abs(self.y - y)
        if d <= 0:
            return EmptyRange()
        return Range(self.x - d, self.x + d)


@dataclass
class Area:
    left: int
    top: int
    right: int
    bottom: int


class EmptyRange:
    def __add__(self, other):
        return other


@dataclass
class Range:
    left:int
    right:int

    def __len__(self):
        return self.right - self.left

    def is_overwrap(self, other):
        if type(other) is EmptyRange:
            return True
        return self.left <= other.right and other.left <= self.right

    def __add__(self, other):
        if type(other) is EmptyRange:
            return self
        if self.is_overwrap(other):
            return Range(min(self.left, other.left), max(self.right, other.right))
        return CombinedRange([self, other])


class CombinedRange:
    def __init__(self, ranges):
        self._ranges = ranges[:]

    @staticmethod
    def _add_range(ranges, other):
        while True:
            for i, r in enumerate(ranges):
                if r.is_overwrap(other):
                    ranges[i] = r + other
                    other = ranges.pop(i)
                    break
            else:
                ranges.append(other)
                return ranges

    def __add__(self, other):
        ranges = self._ranges[:]
        ranges = self._add_range(ranges, other)
        return CombinedRange(ranges)

    def __len__(self):
        return sum([len(r) for r in self._ranges])

    def __repr__(self):
        return f"CombinedRange({self._ranges})"


def test_combined_range():
    assert len(CombinedRange([Range(1,10)]) + Range(5, 15)) == 14
    r = CombinedRange([Range(1,10)]) + Range(15, 20)
    assert len(r) == 14


def test_read():
    line = "Sensor at x=346753, y=3974683: closest beacon is at x=527500, y=3570474"
    expected = Sensor(x=346753, y=3974683, beacon_x=527500, beacon_y=3570474)
    assert read(line) == expected


def test_read_with_minus():
    line = "Sensor at x=303245, y=10539: closest beacon is at x=-171619, y=497931"
    expected = Sensor(x=303245, y=10539, beacon_x=-171619, beacon_y=497931)
    assert read(line) == expected


def test_map():
    sensors = [
        Sensor(5, 5, 2, 3),
    ]
    expected = [
        '.....#....',
        '....###...',
        '...#####..',
        '..B######.',
        '.#########',
        '##########',
        '.#########',
        '..#######.',
        '...#####..',
        '....###...',
    ]
    print(draw_map(sensors, Area(0, 0, 10, 10)))
    assert draw_map(sensors, Area(0, 0, 10, 10)) == expected


def test_covered_area():
    sensors = [Sensor(0, 10, 0, 11), Sensor(10, 0, 10, 1)]
    assert Area(-1, -1, 12, 12) == covered_area(sensors)



def read(input_line)->Sensor:
    parsed = re.match(r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)", input_line).groups()
    return Sensor(x=int(parsed[0]), y=int(parsed[1]),
                  beacon_x=int(parsed[2]), beacon_y=int(parsed[3]))


def get_cell(sensors, x, y)->str:
    for sensor in sensors:
        if (x, y) == (sensor.beacon_x, sensor.beacon_y):
            return 'B'
    for sensor in sensors:
        if distance(x, y, sensor.x, sensor.y) <= sensor.distance():
            return '#'
    else:
        return '.'


def draw_map(sensors, area)->list[str]:
    mapped = []
    for y in range(area.top, area.bottom):
        s = ''
        for x in range(area.left, area.right):
            s += get_cell(sensors, x, y)
        mapped.append(s)
    return mapped


def covered_area(sensors):
    areas = [s.cover_area() for s in sensors]
    return Area(min([a.left for a in areas]),
                min([a.top for a in areas]),
                max([a.right for a in areas]) + 1,
                max([a.bottom for a in areas]) + 1)


def count_no_beacon(sensors, area, y):
#    count = 0
#    for x in range(area.left, area.right):
#        if get_cell(sensors, x, y) == '#':
#            count += 1
#    return count
    return len(calc_range_for_row(sensors, y))


def calc_range_for_row(sensors, y):
    r = EmptyRange()
    for s in sensors:
        rr = s.get_row(y)
        if rr:
            r += rr
    return r


def find_undetected_beacon(sensors, area):
    for y in range(area.top, area.bottom):
        rng = calc_range_for_row(sensors, y=y)
        if type(rng) is CombinedRange and len(rng._ranges) > 1:
            break
    else:
        return None
    return (rng._ranges[0].right + 1, y)


def tune(x, y):
    return x * 4000000 + y


def test_sample1():
    lines = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
    sensors = [read(s.strip()) for s in lines.split('\n') if len(s) > 0]
    print(sensors)
    area = covered_area(sensors)
    print(area)
    mapped = draw_map(sensors, area)
    for l in mapped:
        print(l)
    assert count_no_beacon(sensors, area, y=10) == 26
    x, y = find_undetected_beacon(sensors, Area(0, 0, 21, 21))
    assert (x, y) == (14, 11)
    assert tune(x, y) == 56000011


def test_sample2():
    lines = '''
Sensor at x=346753, y=3974683: closest beacon is at x=527500, y=3570474
Sensor at x=3718952, y=2421864: closest beacon is at x=3871651, y=2935623
Sensor at x=919295, y=2535231: closest beacon is at x=527500, y=3570474
Sensor at x=3982082, y=2935124: closest beacon is at x=3871651, y=2935623
Sensor at x=3693260, y=3095908: closest beacon is at x=3669901, y=3086819
Sensor at x=3273954, y=2072378: closest beacon is at x=3275433, y=2000000
Sensor at x=2936799, y=2402146: closest beacon is at x=2472215, y=2601723
Sensor at x=3153125, y=3571786: closest beacon is at x=3669901, y=3086819
Sensor at x=3892050, y=3718400: closest beacon is at x=3871651, y=2935623
Sensor at x=1670487, y=618098: closest beacon is at x=-171619, y=497931
Sensor at x=277848, y=3523156: closest beacon is at x=527500, y=3570474
Sensor at x=3412305, y=198361: closest beacon is at x=3275433, y=2000000
Sensor at x=2324630, y=2084344: closest beacon is at x=2472215, y=2601723
Sensor at x=3718763, y=3088136: closest beacon is at x=3669901, y=3086819
Sensor at x=303245, y=10539: closest beacon is at x=-171619, y=497931
Sensor at x=3230426, y=1961497: closest beacon is at x=3275433, y=2000000
Sensor at x=3616662, y=3171194: closest beacon is at x=3669901, y=3086819
Sensor at x=3673367, y=3084002: closest beacon is at x=3669901, y=3086819
Sensor at x=3350734, y=2116841: closest beacon is at x=3275433, y=2000000
Sensor at x=1348476, y=3646233: closest beacon is at x=527500, y=3570474
Sensor at x=2817552, y=1654754: closest beacon is at x=3275433, y=2000000
Sensor at x=22462, y=1187401: closest beacon is at x=-171619, y=497931
Sensor at x=3982255, y=1687776: closest beacon is at x=3275433, y=2000000
Sensor at x=3995256, y=2821993: closest beacon is at x=3871651, y=2935623
Sensor at x=501107, y=3777047: closest beacon is at x=527500, y=3570474
Sensor at x=2507803, y=2761101: closest beacon is at x=2472215, y=2601723
Sensor at x=2252560, y=2800057: closest beacon is at x=2370240, y=2923480
Sensor at x=3536077, y=2843837: closest beacon is at x=3669901, y=3086819
Sensor at x=533494, y=3224642: closest beacon is at x=527500, y=3570474
Sensor at x=2962174, y=3016018: closest beacon is at x=2370240, y=2923480
Sensor at x=177378, y=3319282: closest beacon is at x=527500, y=3570474
Sensor at x=2074019, y=3934937: closest beacon is at x=2370240, y=2923480
Sensor at x=2295953, y=3295493: closest beacon is at x=2370240, y=2923480
'''
    sensors = [read(s.strip()) for s in lines.split('\n') if len(s) > 0]
    area = covered_area(sensors)
    assert count_no_beacon(sensors, area, y=2000000) == 4737567
    x, y = find_undetected_beacon(sensors, Area(0, 0, 4000001, 4000001))
    assert (x, y) == (3316868, 2686239)
    assert tune(x, y) == 13267474686239

