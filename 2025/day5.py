"""Advent of Code 2025 Day 5."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 5
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

__title__ = "Advent of Code 2025 Day 5"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path


def ranges_overlap(one: range, two: range) -> bool:
    """Return True if ranges overlap."""
    return one.start < two.stop and two.start < one.stop


##def join_overlapping_ranges(original: Iterable[range]) -> list[range]:
##    iter_original = iter(original)
##    new_ranges = [next(iter_original)]
##    for new_range in iter_original:
##        for existing_range in new_ranges:
##            if not ranges_overlap(new_range, existing_range):
##                continue


def join_overlapping_ranges(ranges: list[range]) -> list[range]:
    """Return list of overlapping of non-overlapping ranges."""
    if not ranges:
        return []

    # Sort by start value
    sorted_ranges = sorted(ranges, key=lambda r: r.start)

    merged = [sorted_ranges[0]]

    # Iterate through the remaining ranges
    for current in sorted_ranges[1:]:
        # Get the last range in the merged list
        last = merged[-1]

        # Check if current range overlaps with the last merged range
        if current.start <= last.stop:
            # Merge the ranges by creating a new range with the lowest
            # start and the highest stop
            merged[-1] = range(last.start, max(last.stop, current.stop))
            continue
        merged.append(current)
    return merged


def run() -> None:
    """Run program."""
    # Load data
    data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    data_file = Path(__file__).absolute().parent / "day5.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    ranges: list[range] = []
    available_ids: list[int] = []
    range_mode = True
    # smallest, largest = map(int, data.split("\n", 1)[0].split("-", 1))
    for line in data.splitlines():
        if range_mode:
            if not line:
                range_mode = False
                continue
            start, end = map(int, line.split("-", 1))
            # smallest = min(smallest, start)
            # largest = max(largest, end)
            ranges.append(range(start, end + 1))
        else:
            available_ids.append(int(line))
    # print("\n".join(map(repr, ranges)))
    # print(available_ids)

    fresh_count = 0
    for id_ in available_ids:
        for range_ in ranges:
            if id_ in range_:
                fresh_count += 1
                break
    print(f"{fresh_count = }")

    # print(f'{len(range(smallest, largest+1)) = }')
    combined_ranges = join_overlapping_ranges(ranges)
    fresh_count = 0
    for range_ in combined_ranges:
        fresh_count += len(range_)
    print(f"{fresh_count = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
