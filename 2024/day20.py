"""Advent of Code 2024 Day 20."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 20
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

__title__ = "Advent of Code 2024 Day 20"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence


# Stolen from 2024 Days 6, 10, 12, and 18
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


# Stolen from 2024 Days 10, 12, 14, 15, 16, and 18
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
                buffer += "."  # " "
        buffer += "|\n"
    print(buffer)


def render_matrix(
    matrix: dict[tuple[int, int], int],
    width: int,
    height: int,
) -> None:
    """Render distance matrix."""
    render_map(
        [("O", list(matrix))],
        width,
        height,
    )


def calculate_matrix(
    start: tuple[int, int],
    walls: tuple[tuple[int, int], ...],
    width: int,
    height: int,
) -> dict[tuple[int, int], int]:
    """Return distance matrix given wall tiles and size."""
    matrix: dict[tuple[int, int], int] = {start: 0}
    heads: list[tuple[int, int]] = [start]
    while heads:
        head = heads.pop()
        new_distance = matrix[head] + 1
        edges = get_point_edges(*head)
        for edge in edges:
            x, y = edge
            if x < 0 or x >= width:
                continue
            if y < 0 or y >= height:
                continue
            if edge in walls:
                continue
            old_distance = matrix.get(edge)
            if old_distance is None or old_distance > new_distance:
                matrix[edge] = new_distance
                heads.append(edge)
    return matrix


def find_starts(
    matrix: dict[tuple[int, int], int],
    width: int,
    height: int,
) -> Generator[tuple[int, tuple[int, int]], None, None]:
    """Yield tuples of distance from start and valid edges of start point."""
    for point in matrix:
        for edge in get_point_edges(*point):
            ex, ey = edge
            if ex < 0 or ex >= width:
                continue
            if ey < 0 or ey >= height:
                continue
            if matrix.get(edge) is not None:
                continue
            yield matrix[point], edge


def find_useful_cheats(
    matrix: dict[tuple[int, int], int],
    width: int,
    height: int,
) -> Generator[tuple[int, int], None, None]:
    """Yield tuples of cheat 0 distance and end cheat distance."""
    for path_start, cheat_start in find_starts(matrix, width, height):
        for edge in get_point_edges(*cheat_start):
            x, y = edge
            if x < 0 or x >= width:
                continue
            if y < 0 or y >= height:
                continue
            edge_dist = matrix.get(edge)
            if edge_dist is None:
                continue
            if edge_dist >= path_start:
                continue
            yield (path_start, edge_dist)


def find_cheat_links(
    distance_matrix: dict[tuple[int, int], int],
    max_distance: int = 20,
) -> Generator[tuple[int, int, int], None, None]:
    """Yield tuples of start distance, end distance, and manhattan distance between start and end."""
    for (x1, y1), start_dist in distance_matrix.items():
        for (x2, y2), end_dist in distance_matrix.items():
            if x1 == x2 and y1 == y2:
                continue
            manhattan_dist = abs(x1 - x2) + abs(y1 - y2)
            if manhattan_dist > max_distance:
                continue
            if end_dist < start_dist:
                continue
            yield (start_dist, end_dist, manhattan_dist)


def run() -> None:
    """Run program."""
    data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    data_file = Path(__file__).absolute().parent / "day20.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    # Read map
    start = (0, 0)
    end = (0, 0)
    walls: list[tuple[int, int]] = []
    y = 0
    line = ""
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == ".":
                continue
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
            elif char == "#":
                walls.append((x, y))
    width = len(line) + 1
    height = y + 1

    distance_matrix = calculate_matrix(start, tuple(walls), width, height)
    original_dist = distance_matrix[end]
    print(f"{original_dist = }")
    ##render_map(
    ##    [("O", [pos for pos in distance_matrix])],
    ##    width,
    ##    height,
    ##)

    ##saved_count: Counter[int] = Counter()
    count = 0
    for start_dist, end_dist, dist in find_cheat_links(distance_matrix, 2):
        saved = end_dist - start_dist - dist

        if saved <= 0:
            continue

        # saved_count[saved] += 1
        if saved >= 100:
            count += 1
    ##for saved in sorted(saved_count):
    ##    print(f'{saved_count[saved]} cheats that save {saved}')
    print(f"{count = }")

    ##saved_count.clear()
    count = 0
    for start_dist, end_dist, dist in set(find_cheat_links(distance_matrix)):
        saved = end_dist - start_dist - dist

        if saved <= 0:
            continue

        ##if saved >= 50:
        ##    saved_count[saved] += 1
        if saved >= 100:
            count += 1
    ##for saved in sorted(saved_count):
    ##    print(f'{saved_count[saved]} cheats that save {saved}')
    print(f"{count = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
