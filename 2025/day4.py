"""Advent of Code 2025 Day 4."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 4
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

__title__ = "Advent of Code 2025 Day 4"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable, Sequence


def get_sides(cx: int, cy: int) -> Generator[tuple[int, int], None, None]:
    """Yield all 8 sides of given center position."""
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if not dx and not dy:
                continue
            yield (cx + dx, cy + dy)


def remove_invalid(
    positions: Iterable[tuple[int, int]],
    width: int,
    height: int,
) -> Generator[tuple[int, int], None, None]:
    """Yield valid positions."""
    for x, y in positions:
        if x < 0 or x >= width:
            continue
        if y < 0 or y >= height:
            continue
        yield x, y


def get_surrounding_type_count(
    map_: Sequence[str],
    position: tuple[int, int],
    type_: str = "@",
) -> int:
    """Return the number of given type in map surrounding given position."""
    height = len(map_)
    width = len(map_[0])

    count = 0
    for x, y in remove_invalid(get_sides(*position), width, height):
        if map_[y][x] == type_:
            count += 1
    return count


def run() -> None:
    """Run program."""
    # Load data
    data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    data_file = Path(__file__).absolute().parent / "day4.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    lines = data.splitlines()

    # print("\n".join(lines))
    height = len(lines)
    width = len(lines[0])

    first_tick = True
    count = 0

    continue_ticking = True

    while continue_ticking:
        continue_ticking = False
        new_map = []

        for y in range(height):
            line = ""
            for x in range(width):
                if (
                    lines[y][x] == "@"
                    and get_surrounding_type_count(lines, (x, y)) < 4
                ):
                    count += 1
                    line += "."  #'x'
                    continue_ticking = True
                else:
                    line += lines[y][x]
            new_map.append(line)
        lines = new_map
        # print('\n'.join(new_map))
        if first_tick:
            print(f"{count = }")
            first_tick = False
    print(f"{count = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
