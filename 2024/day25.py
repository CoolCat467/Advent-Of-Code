"""Advent of Code 2024 Day 25."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 25
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

__title__ = "Advent of Code 2024 Day 25"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path


def invert_column(column: tuple[int, ...]) -> tuple[int, ...]:
    """Return column data inverted (ie key -> lock or lock -> key)."""
    return tuple(5 - x for x in column)


def run() -> None:
    """Run program."""
    data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    data_file = Path(__file__).absolute().parent / "day25.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    locks: list[tuple[int, ...]] = []
    keys: list[tuple[int, ...]] = []
    for block in data.split("\n\n"):
        lines = block.splitlines()

        is_lock = next(iter(set(lines[0]))) == "#"
        lines = lines[1:-1] if is_lock else lines[-2:0:-1]
        column = [0] * len(lines[0])
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    column[x] = y + 1
        if is_lock:
            locks.append(tuple(column))
        else:
            keys.append(tuple(column))

    fit_no_overlap = 0
    for lock in locks:
        for key in keys:
            lock_key = invert_column(lock)
            for x, y in zip(key, lock_key, strict=True):
                if x > y:
                    # print(f"Overlap Column {idx+1}")
                    break
            else:
                fit_no_overlap += 1
                # print("Fits!")
    print(f"{fit_no_overlap = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
