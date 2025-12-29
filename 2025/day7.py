"""Advent of Code 2025 Day 7."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 7
# Copyright (C) 2025  CoolCat467
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

__title__ = "Advent of Code 2025 Day 7"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections import Counter
from pathlib import Path


def run() -> None:
    """Run program."""
    # Load data
    data = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    data_file = Path(__file__).absolute().parent / "day7.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    start_line, *lines = data.splitlines()
    start_pos = start_line.index("S")
    rows: list[set[int]] = []
    for line in lines:
        row: set[int] = set()
        for column, char in enumerate(line):
            if char != "^":
                continue
            row.add(column)
        if not row:
            continue
        rows.append(row)
    # print('\n'.join(map(repr, rows)))

    # Part 1
    hit = 0
    current_beams = {start_pos}
    for row in rows:
        hit_splitters = row & current_beams
        current_beams -= hit_splitters
        for column in hit_splitters:
            current_beams |= {column - 1, column + 1}
        hit += len(hit_splitters)
        # print(f'{current = }')
    print(f"{hit = }")

    # Part 2
    current_beam_timelines = Counter((start_pos,))
    for row in rows:
        # print(f'{set(column_timelines) = }')
        hit_splitters = row & set(current_beam_timelines)
        for column in hit_splitters:
            count = current_beam_timelines.pop(column)
            current_beam_timelines[column - 1] += count
            current_beam_timelines[column + 1] += count
    print(f"{sum(current_beam_timelines.values()) = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
