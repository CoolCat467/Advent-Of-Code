"""Advent of Code 2024 Day 21."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 21
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

__title__ = "Advent of Code 2024 Day 21"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


def find_button_pos(target_char: str, buttons: list[str]) -> tuple[int, int]:
    """Return position of target button in buttons.

    Raises ValueError if button does not exist.
    """
    for y, line in enumerate(buttons):
        for x, char in enumerate(line):
            if char == target_char:
                return (x, y)
    raise ValueError(f"{target_char!r} not found")


def yield_presses(
    sequence: Iterable[str],
    buttons: list[str],
) -> Generator[str, None, None]:
    """Yield sequence of buttons presses to enter given sequence with given button panel."""
    cx, cy = find_button_pos("A", buttons)
    for item in sequence:
        tx, ty = find_button_pos(item, buttons)
        while cx != tx or cy != ty:
            if cx > tx and (buttons[cy][cx - 1] != " "):
                yield "<"
                cx -= 1
            elif cx < tx and (buttons[cy][cx + 1] != " "):
                yield ">"
                cx += 1
            elif cy < ty and (buttons[cy + 1][cx] != " "):
                yield "v"
                cy += 1
            elif cy > ty and (buttons[cy - 1][cx] != " "):
                yield "^"
                cy -= 1
            else:
                raise ValueError
        yield "A"


def calculate_complexity(numeric_code: str, enter_code: str) -> int:
    """Return complexity value."""
    entered = len(enter_code)
    numeric = int(numeric_code.split("A", 1)[0])
    ##    print(f'{entered} * {numeric} = {entered * numeric}')
    return entered * numeric


def run() -> None:
    """Run program."""
    data = """029A
980A
179A
456A
379A"""
    data_file = Path(__file__).absolute().parent / "day21.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    numeric_buttons = "789\n456\n123\n 0A".splitlines()
    direction_buttons = " ^A\n<v>".splitlines()

    complexity = 0
    ##    d2 = """029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    ##980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
    ##179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
    ##456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
    ##379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"""
    ##    for line in d2.splitlines():
    ##        numeric_code, right = line.split(": ", 1)
    ##        print(f"{numeric_code}: {len(right) = }")
    ##        print(right)
    ##        ##
    ##        ##        print("###")
    for numeric_code in data.splitlines():
        print(numeric_code)
        directional_code = "".join(
            yield_presses(numeric_code, numeric_buttons),
        )
        print(directional_code)
        directional_code = "".join(
            yield_presses(directional_code, direction_buttons),
        )
        print(directional_code)
        directional_code = "".join(
            yield_presses(directional_code, direction_buttons),
        )
        print(directional_code)
        ##print(f'{third}\n{len(third) = }')
        complexity += calculate_complexity(numeric_code, directional_code)
        print(f"{numeric_code}: {len(directional_code) = }")
        print()
    ##        break
    print(f"{complexity = }")

    # 127066 too high


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
