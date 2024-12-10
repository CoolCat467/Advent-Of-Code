"""Advent of Code 2024 Day 10."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 10
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

__title__ = "Advent of Code 2024 Day 10"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Generator,
        Sequence,
    )


def get_point_edges(
    x: int,
    y: int,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Return edges of given point."""
    return (
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    )


def find_trail_heads(
    map_: list[str],
) -> Generator[tuple[int, int], None, None]:
    """Yield trail head positions."""
    for y, line in enumerate(map_):
        for x, char in enumerate(line):
            if char == "0":
                yield (x, y)


def continue_trail(
    map_: list[str],
    current: tuple[int, int],
) -> Generator[tuple[tuple[int, int], ...], None, None]:
    """Continue trail given map and current position."""
    x, y = current
    current_num = int(map_[y][x])
    if current_num == 9:
        yield ()
    else:
        next_num = str(current_num + 1)
        for pos in get_point_edges(x, y):
            x, y = pos
            if y < 0 or x < 0 or y >= len(map_):
                continue
            line = map_[y]
            if x >= len(line):
                continue
            if line[x] != next_num:
                continue
            for new_pos in continue_trail(map_, pos):
                yield (pos, *new_pos)


def render_map(points: Sequence[tuple[int, int]], w: int, h: int) -> None:
    """Render map."""
    buffer = ""
    for y in range(h):
        for x in range(w):
            if (x, y) in points:
                buffer += str(points.index((x, y)))
                continue
            buffer += " "
        buffer += "|\n"
    print(buffer)


def find_trails(map_: list[str]) -> tuple[int, int]:
    """Solve part 1 and 2."""
    total_scores = 0
    total_ratings = 0
    for pos in find_trail_heads(map_):
        trail_rating = 0
        unique_ends = set()
        for chain in continue_trail(map_, pos):
            unique_ends.add(chain[-1])
            trail_rating += 1

        trail_score = len(unique_ends)

        total_scores += trail_score
        total_ratings += trail_rating
    return total_scores, total_ratings


def run() -> None:
    """Run program."""
    data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    data_file = Path(__file__).absolute().parent / "day10.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    map_ = data.splitlines()

    print(f"{find_trails(map_) = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
