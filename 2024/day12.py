"""Advent of Code 2024 Day 12."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 12
# Copyright (C) 2024  CoolCat467
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__title__ = "Advent of Code 2024 Day 12"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Generator,
        Sequence,
    )


# Stolen from 2024 Day 6 and 2024 Day 10
def get_point_edges(
    x: int,
    y: int,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Return edges of given point."""
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )


# Stolen from 2024 Day 6
def is_out_of_bounds(x: int, y: int, w: int, h: int) -> bool:
    """Return if given position is out of bounds."""
    return (x < 0 or x >= w) or (y < 0 or y >= h)


def yield_line(x: int, y: int, direction: int) -> Generator[tuple[int, int]]:
    """Yield points in direction along line starting and including given position."""
    while True:
        yield x, y
        x, y = get_point_edges(x, y)[direction]


def identify_sides(
    sides_count: Counter[tuple[int, int]],
    width: int,
    height: int,
) -> int:
    """Return number of sides shape has."""
    sides = 0
    points_in_sides: set[tuple[int, int]] = set()

    edge_group_items: list[tuple[int, set[tuple[int, int]]]] = []

    edge_groups: list[tuple[str, set[tuple[int, int]]]] = []
    edge_counts: dict[int, int] = {}

    for y in range(-1, height + 1):
        for x in range(-1, width + 1):
            point = (x, y)
            point_count = sides_count[point]
            if not point_count:
                continue
            ##    for point, point_count in sides_count.items():
            valid_directions = []
            for direction, edge_point in enumerate(get_point_edges(*point)):
                if edge_point in sides_count:
                    valid_directions.append(direction)
            if not valid_directions:
                sides += point_count
                edge_counts[len(edge_groups)] = point_count
                edge_groups.append((str(point_count), {point}))
                ##                edge_groups.append((str(len(edge_groups)), (point,)))
                continue
            ##            print(f'{point = } {valid_directions = }')
            for direction in valid_directions:
                groupped_edges = set()
                all_already_exist = True
                min_count = point_count
                for edge_point in yield_line(*point, direction):
                    edge_count = sides_count[edge_point]
                    ##                    if edge_point not in sides_count:
                    ##                        break
                    if edge_count == 0:
                        break
                    if edge_count < min_count:
                        ##                        print("click")
                        sides += 1
                    min_count = min(min_count, edge_count)
                    if all_already_exist and edge_point not in points_in_sides:
                        all_already_exist = False
                    groupped_edges.add(edge_point)
                if all_already_exist:
                    ##                    less_than_all = True
                    ##                    for prev_min_count, prev_edge_group in edge_group_items:
                    ##                        if groupped_edges.issubset(prev_edge_group):
                    ##                            if min_count > prev_min_count:
                    ##                                less_than_all = False
                    ##                                break
                    ##                    if less_than_all:
                    ##                        continue
                    continue
                ##                if len(valid_directions) > 1:
                ##                    print(f'{groupped_edges = }')
                sides += min_count
                points_in_sides |= groupped_edges

                edge_group_items.append((min_count, groupped_edges))

                edge_counts[len(edge_groups)] = min_count
                ##                edge_groups.append((str(len(edge_groups)), groupped_edges))
                edge_groups.append((str(min_count), groupped_edges))

    ##            print(f'{groupped_edges = }')

    ##    render = []
    ##    edge_groups.append(("S", set(sides_count.elements())))
    ##    print("\n".join(map(str, edge_groups)))
    ##    print(f'{edge_counts = }')
    ##    render_map_unbounded(edge_groups)
    return sides


def find_corners(area_points: set[tuple[int, int]], map_: list[str]) -> int:
    """Return number of corners shape defined by area_points has.

    Number of corners is the same as number of sides a shape has.
    """
    ##    height = len(map_)
    ##    width = len(map_[0])

    corners = 0
    for point in sorted(area_points):
        neighbors = 0
        for idx, edge_point in enumerate(get_point_edges(*point)):
            if edge_point in area_points:
                neighbors |= (
                    1 << idx
                )  # Set the bit corresponding to the direction

        # Count corners based on the neighbors configuration
        if neighbors == 0b0000:  # No neighbors
            corners += 4  # 4 corners
        elif neighbors == 0b1111 or neighbors in {
            0b1010,
            0b0101,
        }:  # All neighbors
            corners += 0  # No corners
        elif neighbors in {0b1001, 0b1100, 0b0110, 0b0011}:  # Corner
            corners += 2  # 2 corners
        elif neighbors in {0b1110, 0b0111, 0b1011, 0b1101} or neighbors in {
            0b0111,
            0b1110,
        }:  # T shape
            corners += 3  # 3 corners

    return corners


def find_region_points(
    start_x: int,
    start_y: int,
    map_: list[str],
) -> tuple[set[tuple[int, int]], int, int]:
    """Return tuple region area points set, perimeter of shape, and number of sides shape has."""
    height = len(map_)
    width = len(map_[0])

    perimeter = 0

    target_char = map_[start_y][start_x]
    area_points: set[tuple[int, int]] = set()
    unexplored = [(start_x, start_y)]
    explored_count: Counter[tuple[int, int]] = Counter()
    explored: set[tuple[int, int]] = set()
    while unexplored:
        point = unexplored.pop()
        ##        print("###")
        ##        render_map(
        ##            (
        ##                ("X", (point,)),
        ##                ("U", unexplored),
        ##                ("_", area_points),
        ##                (".", explored),
        ##            ),
        ##            width,
        ##            height,
        ##        )
        explored.add(point)
        explored_count[point] += 1
        x, y = point
        if is_out_of_bounds(x, y, width, height):
            perimeter += 1
            ##            print("bounds perimeter")
            continue
        if map_[y][x] != target_char:
            perimeter += 1
            ##            print("nontarget perimeter")
            continue
        ##        print("area")
        area_points.add(point)
        while point in unexplored:
            unexplored.remove(point)
        unexplored.extend(set(get_point_edges(x, y)) - area_points)

    ##    side_points = explored - area_points
    sides_count = explored_count.copy()
    for area_point in area_points:
        del sides_count[area_point]
    ##    render_map(((target_char, area_points),), width, height)
    ##    render_map_unbounded(((target_char, area_points),))
    ##    print(f'{explored_count = }')
    sides = identify_sides(sides_count, width, height)
    ##    sides = find_corners(area_points, map_)

    assert area_points
    return area_points, perimeter, sides


def identify_regions(
    map_: list[str],
) -> Generator[tuple[str, set[tuple[int, int]], int, int], None, None]:
    """Yield tuples of region character, region area points, region peremiter, and number of sides region has."""
    in_regions: set[tuple[int, int]] = set()
    for y, line in enumerate(map_):
        for x, char in enumerate(line):
            if (x, y) in in_regions:
                continue
            area_points, perimeter, sides = find_region_points(x, y, map_)
            in_regions |= area_points
            yield (char, area_points, perimeter, sides)


# +-+-+-+-+-+
# |O O O O O|
# + +-+ +-+ +
# |O|X|O|X|O|
# + +-+ +-+ +
# |O O O O O|
# + +-+ +-+ +
# |O|X|O|X|O|
# + +-+ +-+ +
# |O O O O O|
# +-+-+-+-+-+


def render_map_unbounded(
    regions: Sequence[tuple[str, Sequence[tuple[int, int]]]],
) -> None:
    """Render map without bounded size, show all points."""
    end_x, end_y = 0, 0
    for _char, points in regions:
        for x, y in points:
            end_x = max(end_x, x)
            end_y = max(end_y, y)
    start_x, start_y = end_x, end_y
    for _char, points in regions:
        for x, y in points:
            start_x = min(start_x, x)
            start_y = min(start_y, y)
    buffer = ""
    for y in range(start_y, end_y + 1):
        for x in range(start_x, end_x + 1):
            for char, points in regions:
                if (x, y) in points:
                    buffer += char
                    break
            else:
                buffer += " "
        buffer += "\n"
    print(buffer)


def render_map(
    regions: Sequence[tuple[str, Sequence[tuple[int, int]]]],
    w: int,
    h: int,
) -> None:
    """Render map."""
    buffer = ""
    for y in range(h):
        for x in range(w):
            for char, points in regions:
                if (x, y) in points:
                    buffer += char
                    break
            else:
                buffer += " "
        buffer += "|\n"
    print(buffer)


def run() -> None:
    """Run program."""
    data = """AAAA
BBCD
BBCC
EEEC"""
    ##    data = """EEEEE
    ##EXXXX
    ##EEEEE
    ##EXXXX
    ##EEEEE"""
    data = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
    ##    data = """OOOOO
    ##OXOXO
    ##OOOOO
    ##OXOXO
    ##OOOOO"""
    ##    data = """RRRRIICCFF
    ##RRRRIICCCF
    ##VVRRRCCFFF
    ##VVRCCCJFFF
    ##VVVVCJJCFE
    ##VVIVCCJJEE
    ##VVIIICJJEE
    ##MIIIIIJJEE
    ##MIIISIJEEE
    ##MMMISSJEEE"""
    data_file = Path(__file__).absolute().parent / "day12.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    map_ = data.splitlines()

    ##height = len(map_)
    ##width = len(map_[0])

    total_price = 0
    total_bulk_discount_price = 0
    for char, area_points, perimeter, sides in identify_regions(map_):
        area = len(area_points)
        ##        print(f'{char = } {area = } {perimeter = }')
        ##        print(f'{area_points = }')
        ##        render_map(((char, area_points),), width, height)
        ##        break
        ##        if char == "B":
        ##            break
        price = area * perimeter
        bulk_discount_price = area * sides
        ##        print(f'{char = } {price = }')
        print(f"{char = } {area = } {sides = }")
        ##        if area != 1:
        ##            correction = input("Correct sides?: ")
        ##            if correction:
        ##                sides = int(correction)
        ##                bulk_discount_price = area * sides
        total_price += price
        total_bulk_discount_price += bulk_discount_price
    ##        break
    print(f"{total_price = }")
    print(f"{total_bulk_discount_price = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
