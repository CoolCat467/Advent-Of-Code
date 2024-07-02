#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 15

"Advent of Code 2022 Day 15."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 15"
__author__ = "CoolCat467"
__version__ = "0.0.0"


import dataclasses
import io
from typing import Iterable, Iterator


@dataclasses.dataclass(slots=True)
class Point:
    "Represents a two dimensional point."  # noqa: D300
    x: int
    y: int

    def __iter__(self) -> Iterator[int]:  # noqa: D105
        return iter((self.x, self.y))

    def __getitem__(self, index: int) -> int:  # noqa: D105
        return (self.x, self.y)[index]

    def __add__(self, obj: Iterable[int]) -> Point:  # noqa: D105
        gen = iter(obj)
        return Point(self.x + next(gen), self.y + next(gen))

    def __iadd__(self, obj: Iterable[int]) -> Point:  # noqa: PYI034, D105
        gen = iter(obj)
        self.x += next(gen)
        self.y += next(gen)
        return self

    def __sub__(self, obj: Iterable[int]) -> Point:  # noqa: D105
        gen = iter(obj)
        return Point(self.x - next(gen), self.y - next(gen))

    def as_tuple(self) -> tuple[int, int]:
        "Get point as tuple."  # noqa: D300
        return self.x, self.y

    def __abs__(self) -> Point:  # noqa: D105
        return Point(abs(self.x), abs(self.y))

    def __copy__(self) -> Point:  # noqa: D105
        return Point(self.x, self.y)

    copy = __copy__


def find_viewport(
    points: Iterable[tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    "Find view port area for given points."  # noqa: D300
    x, y = next(iter(points))
    minmax = [[x, x], [y, y]]
    for point in points:
        for i in range(2):
            if point[i] < minmax[i][0]:
                minmax[i][0] = point[i]
            if point[i] > minmax[i][1]:
                minmax[i][1] = point[i]
    return (minmax[0][0], minmax[0][1]), (minmax[1][0], minmax[1][1])


def print_map(
    sensors: set[tuple[int, int]],
    beacons: set[tuple[int, int]],
    scan_area: set[tuple[int, int]],
) -> None:
    "Print the map of the world."  # noqa: D300
    all_points = sensors | beacons | scan_area
    x_view, y_view = find_viewport(all_points)
    minx, maxx = x_view
    miny, maxy = y_view
    # Only do one print call to speed it up
    lines = ""
    y_digits = max(len(str(miny - 1)), len(str(maxy + 1)))
    for y in range(miny - 1, maxy + 2):
        lines += str(y).rjust(y_digits) + " "
        for x in range(minx - 1, maxx + 2):
            point = (x, y)
            if point in beacons:
                lines += "B"
            elif point in sensors:
                lines += "S"
            elif point in scan_area:
                lines += "#"
            else:
                lines += "."
        lines += "\n"
    print(lines)


def sensor_area(location: Point, distance: int) -> set[tuple[int, int]]:
    "Get sensor area for point."  # noqa: D300
    points: set[tuple[int, int]] = set()
    for y in range(-distance, distance + 1):
        for x in range(-distance, distance + 1):
            if abs(x) + abs(y) <= distance:
                points.add(((*location, x, y)).as_tuple())
    return points


def sensor_area_at_y(
    location: Point,
    distance: int,
    y_pos: int,
) -> set[tuple[int, int]]:
    "Get sensor area for point where y == y_pos."  # noqa: D300
    points: set[tuple[int, int]] = set()
    y = y_pos - location.y
    for x in range(-distance, distance + 1):
        if abs(x) + abs(y) <= distance:
            new = (*location, x, y)
            points.add(new.as_tuple())
    return points


def sensor_area_square_at_y(
    location: Point,
    distance: int,
    y_pos: int,
    find: set[int],
) -> set[int]:
    "Get sensor area for point where y == y_pos."  # noqa: D300
    points: set[int] = set()
    y = y_pos - location.y
    x_min = -max(distance, location.x, min(find))
    x_max = min(distance, max(find)) + 1
    for x in range(x_min, x_max):
        if abs(x) + abs(y) <= distance:
            ##            new = location + (x, y)
            ##            points.add(new.as_tuple())
            points.add(location.x + x)
    return points


def value_in_range(value: int, start: int, end: int) -> bool:
    "Return if value is within start to end range."  # noqa: D300
    if value < start:
        return False
    return value <= end


def print_sensors(
    sensor_data: list[tuple[tuple[int, int], tuple[int, int]]],
) -> None:
    "Debug print sensors."  # noqa: D300
    sensors: set[tuple[int, int]] = set()
    beacons: set[tuple[int, int]] = set()
    scan_area: set[tuple[int, int]] = set()
    for location, beacon in ((Point(*v) for v in p) for p in sensor_data):
        distance = sum(abs(location - beacon))
        sensors.add(location.as_tuple())
        beacons.add(beacon.as_tuple())
        scan_area |= sensor_area(location, distance)
    print_map(sensors, beacons, scan_area)


def part_one(
    sensor_data: list[tuple[tuple[int, int], tuple[int, int]]],
    target_y: int,
) -> int:
    "Find number of points at target_y that beacon can for sure not be in."  # noqa: D300
    sensors: set[tuple[int, int]] = set()
    beacons: set[tuple[int, int]] = set()
    scan_area: set[tuple[int, int]] = set()
    for location, beacon in ((Point(*v) for v in p) for p in sensor_data):
        distance = sum(abs(location - beacon))
        if value_in_range(
            target_y,
            location.y - distance,
            location.y + distance,
        ):
            if location.y == target_y:
                sensors.add(location.as_tuple())
            if beacon.y == target_y and value_in_range(
                beacon.x,
                location.x - distance,
                location.x + distance,
            ):
                beacons.add(beacon.as_tuple())
            scan_area |= sensor_area_at_y(location, distance, target_y)
    ##    print_map(sensors, beacons, scan_area)
    return len(scan_area - sensors - beacons)


# Would take ~ 3 months in PyPy, and about a year in CPython. Unacceptable.
##def part_two(sensor_data: list[tuple[tuple[int, int], tuple[int, int]]],
##             max_pos: int) -> int:
##    for y in range(max_pos):
##        scan_area: set[int] = set(range(max_pos))
####        print(scan_area)
##        for location, beacon in ((Point(*v) for v in p) for p in sensor_data):
##            distance = sum(abs(location - beacon))
##            exists =  sensor_area_square_at_y(location,
##                                              distance,
##                                              y,
##                                              scan_area)
##            scan_area -= exists
##            if not scan_area:
##                break
####            print_map(set(), set(), {(x, y) for x in exists})
####            print_map(set(), set(), sensor_area(location, distance))
####            print('-'*20)
####            print(exists)
##        print(f'{y}/{max_pos}')
##
##        if scan_area:
##            break
####    print(scan_area)
####    print_map(set(), set(), {(x, y) for x in scan_area})
##    x = scan_area.pop()
####    print((x, y))
##    return x * 4000000 + y
####        print_map(set(), set(), scan_area)


def part_two(
    sensor_data: list[tuple[tuple[int, int], tuple[int, int]]],
    max_pos: int,
) -> int:
    "Find 'tuning frequency' of distress beacon."  # noqa: D300
    # Modified slightly from https://www.reddit.com/r/adventofcode/comments/zmcn64/comment/j0b90nr
    # Much better way of thinking about the problem, you can think of it
    # as 4 line segments at the Manhattan radius. We want to find
    # the position just outside of the radius-es, so just get where
    # intersections happen
    x_coeffs: set[int] = set()
    y_coeffs: set[int] = set()
    distances: dict[tuple[int, int], int] = {}
    for location, beacon in ((Point(*v) for v in p) for p in sensor_data):
        radius = sum(abs(location - beacon))
        x, y = location

        x_coeffs.add(y - x + radius + 1)
        x_coeffs.add(y - x - radius - 1)
        y_coeffs.add(x + y + radius + 1)
        y_coeffs.add(x + y - radius - 1)

        distances[(x, y)] = radius

    for a in x_coeffs:
        for b in y_coeffs:
            # Get point where lines intersect
            point = Point((b - a) // 2, (a + b) // 2)
            # If intersect within bounds
            if all(0 < c < max_pos for c in point):  # noqa: SIM102
                # If intersect is outside of radius for all scanners
                if all(
                    sum(abs(point - loc)) > radius
                    for loc, radius in distances.items()
                ):
                    # This is target
                    x, y = point
                    return x * 4000000 + y
    return 0


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
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
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

    file = io.StringIO(test_data)
    ##    file = open('day15.txt', encoding='utf-8')

    sensors: list[tuple[tuple[int, int], tuple[int, int]]] = []

    for line in file:
        data = line.removeprefix("Sensor at ")
        loc, data = data.split(":")
        x, y = (int(v.split("=")[1]) for v in loc.split(", "))
        location = (x, y)
        data = data.removeprefix(" closest beacon is at ")
        x, y = (int(v.split("=")[1]) for v in data.split(", "))
        closest = (x, y)
        sensors.append((location, closest))

    file.close()

    print(f"{part_one(sensors, 10) = }")
    print(f"{part_two(sensors, 20) = }")


##    print(f'{part_one(sensors, 2000000) = }')
##    print(f'{part_two(sensors, 4000000) = }')


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
