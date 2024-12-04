"""Advent of Code 2024 Day 3."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 3
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

__title__ = "Advent of Code 2024 Day 3"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


import re
from functools import reduce
from operator import mul
from pathlib import Path

PART_ONE_MATCH = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
PART_TWO_MATCH = re.compile(
    r"(?:mul\((\d{1,3}),(\d{1,3})\))|(?:do\(\))|(?:don't\(\))",
)


def handle_instructions_p1(instructions: str) -> int:
    """Handle multiply instructions for part one."""
    total = 0
    for match in PART_ONE_MATCH.finditer(instructions):
        total += reduce(mul, map(int, match.groups()))
    return total


def handle_instructions_p2(instructions: str) -> int:
    """Handle multiply instructions for part one."""
    total = 0
    enable = True
    for match in PART_TWO_MATCH.finditer(instructions):
        start, end = match.span()
        matched = match.string[start:end]
        if matched == "do()":
            enable = True
            continue
        if matched == "don't()":
            enable = False
            continue
        if enable:
            total += reduce(mul, map(int, match.groups()))
    return total


def run() -> None:
    """Run program."""
    # data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    data = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    data = Path("day3.txt").read_text()
    part_one = handle_instructions_p1(data)
    print(f"{part_one = }")
    part_two = handle_instructions_p2(data)
    print(f"{part_two = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
