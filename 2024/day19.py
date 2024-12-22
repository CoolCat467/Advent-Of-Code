"""Advent of Code 2024 Day 19."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 19
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

__title__ = "Advent of Code 2024 Day 19"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def yield_order(
    pattern: str,
    towels: tuple[str, ...],
) -> Generator[tuple[str, ...], None, None]:
    """Yield possible pattern solution orders."""
    if pattern:
        for towel in towels:
            if pattern.startswith(towel):
                post = pattern.removeprefix(towel)
                for order in yield_order(post, towels):
                    yield (pattern, *order)
    else:
        yield ()


def can_make_pattern(pattern: str, towels: tuple[str, ...]) -> bool:
    """Return if able to create pattern given towels."""
    heads: set[str] = {pattern}
    used = tuple(towel for towel in towels if towel in pattern)
    while heads:
        head = heads.pop()
        for towel in used:
            if head.startswith(towel):
                new = head.removeprefix(towel)
                if new == "":
                    return True
                heads.add(new)
    return False


def find_possible_pattern_counts(
    pattern: str,
    towels: tuple[str, ...],
) -> int:
    """Return number of possible ways to form pattern given pattern parts."""
    used = tuple(towel for towel in towels if towel in pattern)

    # Created with help from ChatGPT-4o

    # Create a dynamic programming array to store the number of ways to
    # form each prefix of the pattern
    pattern_counts = [0] * (len(pattern) + 1)
    # Base case: one way to form an empty pattern
    pattern_counts[0] = 1

    for i in range(1, len(pattern) + 1):
        for towel in used:
            towel_length = len(towel)
            # If current item is long enough to form pattern,
            # and if last characters match current towel
            if i >= towel_length and pattern[i - towel_length : i] == towel:
                # Increment number of ways up to here in pattern can be made
                pattern_counts[i] += pattern_counts[i - towel_length]

    return pattern_counts[len(pattern)]


def run() -> None:
    """Run program."""
    data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    data_file = Path(__file__).absolute().parent / "day19.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    gen = iter(data.splitlines())
    towels = tuple(next(gen).split(", "))
    assert not next(gen)
    patterns = tuple(line for line in gen)

    success = 0
    for pattern in patterns:
        if can_make_pattern(pattern, towels):
            success += 1
    print(f"{success = }")

    counts = 0
    for pattern in patterns:
        counts += find_possible_pattern_counts(pattern, towels)
    print(f"{counts = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
