"""Advent of Code 2025 Day 1."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 1
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

__title__ = "Advent of Code 2025 Day 1"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@dataclass
class DialSafe:
    """Rotary Dial Safe."""

    value: int
    max_: int = 99

    def right(self, distance: int) -> int:
        """Rotate to the right given distance. Return new value."""
        self.value += distance
        self.value %= self.max_ + 1
        return self.value

    def left(self, distance: int) -> int:
        """Rotate to the left given distance. Return new value."""
        return self.right(-distance)

    def read_line(self, line: str) -> int:
        """Read line and rotate. Return new value."""
        direction = line[0]
        distance = int(line[1:])
        if direction == "L":
            return self.left(distance)
        if direction == "R":
            return self.right(distance)
        raise NotImplementedError(f"direction {direction!r} ({line = }")

    def yield_right(self, distance: int) -> Generator[int, None, None]:
        """Yield values as rotating to the right given distance."""
        for _ in range(distance):
            self.value += 1
            self.value %= self.max_ + 1
            yield self.value

    def yield_left(self, distance: int) -> Generator[int, None, None]:
        """Yield values as rotating to the left given distance."""
        for _ in range(distance):
            self.value -= 1
            self.value %= self.max_ + 1
            yield self.value

    def read_line_yield(self, line: str) -> Generator[int, None, None]:
        """Yield values as rotating direction given line."""
        direction = line[0]
        distance = int(line[1:])
        if direction == "L":
            yield from self.yield_left(distance)
            return
        if direction == "R":
            yield from self.yield_right(distance)
            return
        raise NotImplementedError(f"direction {direction!r} ({line = }")


def run() -> None:
    """Run program."""
    # Load data
    data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    data_file = Path(__file__).absolute().parent / "day1.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Part 1
    dial = DialSafe(50)
    zero_count = 0
    for line in data.splitlines():
        if dial.read_line(line) == 0:
            zero_count += 1
    print(f"{zero_count = }")

    # Part 2
    dial = DialSafe(50)
    zero_count = 0
    for line in data.splitlines():
        for value in dial.read_line_yield(line):
            if value == 0:
                zero_count += 1
    print(f"{zero_count = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
