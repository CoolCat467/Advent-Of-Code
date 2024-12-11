"""Advent of Code 2024 Day 11."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 11
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

__title__ = "Advent of Code 2024 Day 11"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Generator,
        Iterable,
    )


def tick_step(numbers: Iterable[int]) -> Generator[int, None, None]:
    """Tick pluto rock numbers."""
    for number in numbers:
        as_str = str(number)
        if number == 0:
            yield 1
        elif len(as_str) % 2 == 0:
            # Even number of digits
            middle = len(as_str) // 2
            yield int(as_str[:middle])
            yield int(as_str[middle:])
        else:
            yield number * 2024


def tick_step_counter(numbers: Counter[int]) -> Counter[int]:
    """Tick step but apply to all numbers at once."""
    next_: Counter[int] = Counter()
    for number, count in numbers.items():
        as_str = str(number)
        if number == 0:
            next_[1] += count
        elif len(as_str) % 2 == 0:
            # Even number of digits
            middle = len(as_str) // 2
            next_[int(as_str[:middle])] += count
            next_[int(as_str[middle:])] += count
        else:
            next_[number * 2024] += count
    return next_


def run() -> None:
    """Run program."""
    data = """0 1 10 99 999"""
    data = """125 17"""
    data_file = Path(__file__).absolute().parent / "day11.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    base_numbers = tuple(map(int, data.split(" ")))

    # gen = iter(base_numbers)
    # for step in range(25):
    #     gen = tick_step(gen)
    #
    # item_count = 0
    # for item in gen:
    #     item_count += 1

    count = Counter(base_numbers)
    for _step in range(25):
        count = tick_step_counter(count)

    print(f"{count.total() = }")

    # count = Counter(base_numbers)
    # Can reuse up to 25 data
    for _step in range(75 - 25):
        count = tick_step_counter(count)

    print(f"{count.total() = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
