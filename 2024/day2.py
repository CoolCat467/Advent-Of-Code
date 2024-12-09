"""Advent of Code 2024 Day 2."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 2
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

__title__ = "Advent of Code 2024 Day 2"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


# Stolen from 2023 Day 9
def delta(sequence: Iterable[int]) -> Generator[int, None, None]:
    """Yield deltas between each item in given sequence."""
    gen = iter(sequence)
    prev = next(gen)
    for next_ in gen:
        yield next_ - prev
        prev = next_


def report_is_safe(report: tuple[int, ...]) -> bool:
    """Return if report is safe."""
    diff = tuple(delta(report))
    negative = diff[0] < 0

    for item in diff:
        # If sign is different for any, bad
        if (item < 0) != negative:
            return False
        abs_diff = abs(item)
        if abs_diff < 1:
            return False
        if abs_diff > 3:
            return False

    return True


def report_is_safe_dampened(
    report: tuple[int, ...],
    _recursive: bool = True,
) -> bool:
    """Return if report is safe if dampened."""
    diff = tuple(delta(report))
    negative = diff[0] < 0

    for idx, item in enumerate(diff):
        abs_diff = abs(item)
        # print(f" {item}")
        # If sign is different for any or abs difference is < 1 or > 3, bad
        if (item < 0) != negative or abs_diff < 1 or abs_diff > 3:
            # If already did recursion and still broken, it's unfixable
            if not _recursive:
                return False
            # Otherwise, try removing one item from the report
            for idx in range(len(report)):
                new_report = report[:idx] + report[idx + 1 :]
                if report_is_safe_dampened(new_report, False):
                    # If dampened version is ok, report is ok.
                    return True
            return False
    return True


def run() -> None:
    """Run program."""
    data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    data_file = Path(__file__).absolute().parent / "day2.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    reports = [tuple(map(int, line.split(" "))) for line in data.splitlines()]

    # Keep track of number of safe reports
    safe = 0
    for report in reports:
        if report_is_safe(report):
            safe += 1
    print(f"{safe = }")

    # Find number of safe reports with error dampening
    safe_dampened = 0
    for report in reports:
        if report_is_safe_dampened(report):
            safe_dampened += 1
    print(f"{safe_dampened = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
