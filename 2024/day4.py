"""Advent of Code 2024 Day 4."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 4
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

__title__ = "Advent of Code 2024 Day 4"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

MAS_CROSS = re.compile(r"M.S.A.M.S")


def iter_half_diagonal_chars(
    grid: list[str],
) -> Generator[str | None, None, None]:
    """Yield half diagonal line characters from grid or None to indicate next line."""
    width = len(grid[0])
    height = len(grid)
    for start_y in range(height):
        y = start_y
        x = 0
        while y >= 0 and x < width:
            yield grid[y][x]
            y -= 1
            x += 1
        yield None


def iter_half_diagonal(grid: list[str]) -> Generator[str, None, None]:
    """Yield half diagonal lines from grid."""
    buffer = ""
    for char in iter_half_diagonal_chars(grid):
        if char is None:
            yield buffer
            buffer = ""
        else:
            buffer += char


def iter_diagonal(grid: list[str]) -> Generator[str, None, None]:
    """Yield diagonal line strings grid."""
    for line in iter_half_diagonal(grid[::-1]):
        yield line
    # keeping track of last one
    for rev_line in iter_half_diagonal([line[::-1] for line in grid]):
        # if line is last one, do not duplicate it
        if rev_line == line[::-1]:
            break
        yield rev_line
    assert rev_line == line[::-1], f"{rev_line = } {line[::-1] = }"


def iter_grid(grid: list[str]) -> Generator[str, None, None]:
    """Yield rows, columns, and both diagonals from grid."""
    yield from grid
    width = len(grid[0])
    for col in range(width):
        yield "".join(row[col] for row in grid)
    yield from iter_diagonal(grid)
    yield from iter_diagonal(grid[::-1])


def yield_block_chars(
    grid_x: int,
    grid_y: int,
    grid: list[str],
) -> Generator[str, None, None]:
    """Yield 3x3 block characters with None to indicate next row."""
    for char_x in range(grid_x, grid_x + 3):
        for char_y in range(grid_y, grid_y + 3):
            yield grid[char_y][char_x]
        yield None


def yield_block(
    grid_x: int,
    grid_y: int,
    grid: list[str],
) -> Generator[list[str], None, None]:
    """Yield 3x3 blocks as lists of block row lines."""
    rows = []
    row = ""
    for char in yield_block_chars(grid_x, grid_y, grid):
        if char is not None:
            row += char
        else:
            rows.append(row)
            row = ""
    return rows


def iter_blocks(grid: list[str]) -> Generator[list[str], None, None]:
    """Yield all 3x3 blocks from grid."""
    width = len(grid[0])
    height = len(grid)
    x_blocks = width - 2 if width >= 3 else 0
    y_blocks = height - 2 if height >= 3 else 0
    for x in range(x_blocks):
        for y in range(y_blocks):
            yield yield_block(x, y, grid)


def rotate_block_90(block: list[str]) -> list[str]:
    """Return square text rotated by 90 degrees counterclockwise."""
    return [
        "".join(block[len(block) - 1 - j][i] for j in range(len(block)))
        for i in range(len(block[0]))
    ]


def match_block(block: list[str]) -> bool:
    """Return if block is a MAS cross for exactly one MAS cross orientation."""
    return MAS_CROSS.match("".join(block)) is not None


def match_block_all_rotations(block: list[str]) -> bool:
    """Return if block matches any of the 4 MAS cross orientations."""
    for _ in range(4):
        if match_block(block):
            return True
        block = rotate_block_90(block)
    return False


def run() -> None:
    """Run program."""
    ##    data = """12345
    ##67890
    ##qwert
    ##asdfg
    ##zxcvb""".splitlines()
    data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".splitlines()
    data = Path("day4.txt").read_text().splitlines()
    count = 0
    for orig_line in iter_grid(data):
        for line in (orig_line, orig_line[::-1]):
            count += line.count("XMAS")
    print(f"{count = }")
    block_count = 0
    for block in iter_blocks(data):
        if match_block_all_rotations(block):
            block_count += 1
    print(f"{block_count = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
