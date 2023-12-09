"""Advent of Code 2023 Day 3."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 3"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import re
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator

NUMBER_REGEX: Final = re.compile(r"\d+")


def find_numbers(line: str) -> Iterator[re.Match[str]]:
    """Yield number matches in given line."""
    return NUMBER_REGEX.finditer(line)


def get_outline(
    line_no: int,
    start_col: int,
    stop_col: int,
) -> Generator[tuple[int, int], None, None]:
    """Yield outline (line, column) positions given match (line number, start column, and end column)."""
    for line in range(line_no - 1, line_no + 2):
        for col in range(start_col - 1, stop_col + 1):
            if line == line_no and col >= start_col and col < stop_col:
                continue
            yield (line, col)


def cancel_out_of_bounds(
    gen: Generator[tuple[int, int], None, None],
    start_x: int,
    end_x: int,
    start_y: int,
    end_y: int,
) -> Generator[tuple[int, int], None, None]:
    """Ignore positions that are out of bounds."""
    for x, y in gen:
        if x < start_x or x >= end_x:
            continue
        if y < start_y or y >= end_y:
            continue
        yield (x, y)


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    lines = text.splitlines()

    part_id_sum = 0
    gears: dict[tuple[int, int], list[int]] = {}
    for line_no, line in enumerate(lines):
        numbers = find_numbers(line)
        for match in numbers:
            start, stop = match.span()
            number = int(match.group(0))

            raw_outline = get_outline(line_no, start, stop)
            outline = cancel_out_of_bounds(
                raw_outline,
                0,
                len(line),
                0,
                len(lines),
            )

            for o_line, o_col in outline:
                symbol = lines[o_line][o_col]

                if symbol != ".":
                    part_id_sum += number
                if symbol == "*":
                    gears[(o_line, o_col)] = gears.get((o_line, o_col), [])
                    gears[(o_line, o_col)].append(number)

    gear_ratio_sum = 0
    for _gear_pos, gear_interaction_part_ids in gears.items():
        if len(gear_interaction_part_ids) != 2:
            continue
        one, two = gear_interaction_part_ids
        gear_ratio_sum += one * two

    return part_id_sum, gear_ratio_sum


def run() -> None:
    """Print answer."""
    input_ = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    ##with open("day3.txt", encoding="utf-8") as file:
    ##    input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
