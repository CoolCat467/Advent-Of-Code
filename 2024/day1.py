"""Advent of Code 2024 Day 1."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 1
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

__title__ = "Advent of Code 2024 Day 1"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections import Counter
from pathlib import Path


def run() -> None:
    """Run program."""
    # Load data
    data = """3   4
4   3
2   5
1   3
3   9
3   3"""
    data_file = Path("day1.txt")
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    columns: list[Counter[int]] = [Counter(), Counter()]
    line_no = 0
    for line_no, line in enumerate(data.splitlines()):  # noqa: B007
        for column_id, value in enumerate(map(int, line.split())):
            columns[column_id][value] += 1

    # Save copy for later
    copy = [Counter(dict(x.items())) for x in columns]

    # Calculating total distance between pairs in order
    total_dist = 0
    for _ in range(line_no + 1):
        # Pop left min item
        min_0 = min(columns[0])
        columns[0][min_0] -= 1
        count = columns[0][min_0]
        if not count:
            del columns[0][min_0]

        # Pop right min item
        min_1 = min(columns[1])
        columns[1][min_1] -= 1
        count = columns[1][min_1]
        if not count:
            del columns[1][min_1]

        # Add difference to total distance
        total_dist += abs(min_0 - min_1)
    print(f"{total_dist = }")

    # Restore copy
    columns = copy

    # Find "list similarity"
    similarity = 0
    for number, count in columns[0].items():
        similarity += (number * columns[1][number]) * count
    print(f"{similarity = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
