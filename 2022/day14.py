#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 14

"Advent of Code 2022 Day 14."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 14"
__author__ = "CoolCat467"
__version__ = "0.0.0"


import dataclasses
import io
from typing import Iterable, Iterator, cast


def copysign(x: int, y: int) -> int:
    "Copy sign of y to x."  # noqa: D300
    abs_x = abs(x)
    if y < 0:
        return -abs_x
    if y == 0:
        return x
    return abs_x


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

    def unit_direction(self) -> Point:
        "Get unit direction of point."  # noqa: D300
        return Point(copysign(1, self.x), copysign(1, self.y))

    def __copy__(self) -> Point:  # noqa: D105
        return Point(self.x, self.y)

    copy = __copy__


def points_in_line(line: tuple[tuple[int, int], ...]) -> set[tuple[int, int]]:
    "Calculate the points in a line given the edge points. Only right angles."  # noqa: D300
    last = Point(*line[0])
    points: set[tuple[int, int]] = {line[0]}
    for point in (Point(*v) for v in line[1:]):
        cx, cy = last
        delta = point - last
        dx, dy = delta
        direction = delta.unit_direction()

        if dx != 0:
            x = cx
            change = direction[0]
            for _ in range(abs(dx)):
                x += change
                points.add((x, cy))
        else:
            y = cy
            change = direction[1]
            for _ in range(abs(dy)):
                y += change
                points.add((cx, y))

        last = point
    return points


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
    walls: set[tuple[int, int]],
    sand: tuple[int, int],
    dead_sands: set[tuple[int, int]],
) -> None:
    "Print the map of the world."  # noqa: D300
    all_points = walls | dead_sands | {(500, 0), sand}
    x_view, y_view = find_viewport(all_points)
    minx, maxx = x_view
    miny, maxy = y_view
    # Only do one print call to speed it up
    lines = ""
    for y in range(miny - 1, maxy + 2):
        for x in range(minx - 1, maxx + 2):
            point = (x, y)
            if point in dead_sands:
                lines += "O"
            elif point == sand:
                lines += "+"
            elif point == (500, 0):
                lines += "S"
            elif point in walls:
                lines += "#"
            else:
                lines += "."
        lines += "\n"
    print(lines)


def part_one(lines: list[tuple[tuple[int, int], ...]]) -> int:
    "Calculate many units of sand come to rest before rest falls to abyss."  # noqa: D300
    walls: set[tuple[int, int]] = set()
    for line in lines:
        walls |= points_in_line(line)

    y_dims = find_viewport(walls)[1]
    max_y = y_dims[1] + 1
    ##    print(f'{max_y = }')

    dead_sands: set[tuple[int, int]] = set()
    stops = walls  # Union of walls and dead, but it's own to speed up
    sand = Point(500, 0)
    while sand.y <= max_y:
        if (sand.x, sand.y + 1) not in stops:
            sand.y += 1
        elif (sand.x - 1, sand.y + 1) not in stops:
            sand.x -= 1
            sand.y += 1
        elif (sand.x + 1, sand.y + 1) not in stops:
            sand.x += 1
            sand.y += 1
        else:
            dead_sands.add((sand.x, sand.y))
            stops.add((sand.x, sand.y))
            sand = Point(500, 0)

    ##    print_map(walls, (sand.x, sand.y), dead_sands)
    return len(dead_sands)


def part_two(lines: list[tuple[tuple[int, int], ...]]) -> int:
    "Calculate many units of sand come to rest before sand source is blocked."  # noqa: D300
    walls: set[tuple[int, int]] = set()
    for line in lines:
        walls |= points_in_line(line)

    y_dims = find_viewport(walls)[1]
    max_y = y_dims[1] + 1
    ##    print(f'{max_y = }')

    dead_sands: set[tuple[int, int]] = set()
    sand = Point(500, 0)
    stops = walls  # Union of walls and dead, but it's own to speed up
    while (500, 0) not in dead_sands:
        if sand.y >= max_y:
            dead_sands.add((sand.x, sand.y))
            stops.add((sand.x, sand.y))
            sand = Point(500, 0)
            continue
        if (sand.x, sand.y + 1) not in stops:
            sand.y += 1
        elif (sand.x - 1, sand.y + 1) not in stops:
            sand.x -= 1
            sand.y += 1
        elif (sand.x + 1, sand.y + 1) not in stops:
            sand.x += 1
            sand.y += 1
        else:
            dead_sands.add((sand.x, sand.y))
            stops.add((sand.x, sand.y))
            sand = Point(500, 0)

    ##    print_map(walls, (sand.x, sand.y), dead_sands)
    return len(dead_sands)


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    file = io.StringIO(test_data)
    ##    file = open('day14.txt', encoding='utf-8')

    lines: list[tuple[tuple[int, int], ...]] = []

    for line in file:
        lines.append(
            tuple(
                cast(tuple[int, int], tuple(map(int, v.split(","))))
                for v in line.strip().split(" -> ")
            ),
        )

    file.close()

    print(f"{part_one(lines) = }")
    print(f"{part_two(lines) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
