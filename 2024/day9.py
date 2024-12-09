"""Advent of Code 2024 Day 9."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 9
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

__title__ = "Advent of Code 2024 Day 9"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from time import perf_counter_ns
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Generator,
    )


def expanded(data: str) -> Generator[int | None, None, None]:
    """Yield expanded data values from number."""
    for index, char in enumerate(data):
        len_ = int(char)
        id_: int | None = (index >> 1) if index % 2 == 0 else None
        for _ in range(len_):
            yield id_


def needs_swap(blocks: list[int | None]) -> bool:
    """Return if fragmentation swap should continue."""
    found_blank = False
    for value in blocks:
        if not found_blank and value is None:
            found_blank = True
            continue
        if found_blank and value is not None:
            return True
    return False


def perform_swap(blocks: list[int | None]) -> None:
    """Perfirm fragmentation swap step."""
    blank_start = blocks.index(None)
    pos = 0
    # B007 Loop control variable `pos` not used within loop body
    for pos, char in enumerate(reversed(blocks)):  # noqa: B007
        if char is not None:
            break
    else:
        raise ValueError("No non-blank")
    end = -(pos + 1)
    blocks[blank_start] = blocks[end]
    blocks[end] = None


def calculate_fs_checksum(blocks: list[int | None]) -> int:
    """Return filesystem checksum."""
    checksum = 0
    for index, id_ in enumerate(blocks):
        if id_ is None:
            continue
        checksum += index * id_
    return checksum


def yield_continuous_free(
    blocks: list[int | None],
) -> Generator[tuple[int, int], None, None]:
    """Yield continuous blocks of free space from left."""
    free_count = 0
    for index, block in enumerate(blocks):
        if block is not None:
            if free_count:
                yield index - free_count, free_count
            free_count = 0
        else:
            free_count += 1


def yield_continuous_blocks(
    blocks: list[int | None],
    id_: int,
) -> Generator[tuple[int, int], None, None]:
    """Yield continuous blocks of given id from right."""
    block_count = 0
    block_id: int | None = None
    length = len(blocks)
    for index, block in enumerate(reversed(blocks)):
        if block == block_id:
            block_count += 1
            continue
        if block_count and block_id == id_:
            yield length - index, block_count
        block_count = 1
        block_id = block


def block_swap(blocks: list[int | None], id_: int) -> bool:
    """Perform block swap. Return if needs to continue."""
    for block_start, block_count in yield_continuous_blocks(blocks, id_):
        for free_start, free_count in yield_continuous_free(blocks):
            if free_count < block_count:
                continue
            if block_start < free_start:
                ##print(f"{id_} already moved")
                # continue
                return False
            # free_count >= block_count
            ##print(f"moving {id_} {block_count = } {free_count = }")
            blocks[free_start : free_start + block_count] = blocks[
                block_start : block_start + block_count
            ]
            blocks[block_start : block_start + block_count] = [
                None,
            ] * block_count
            return True
    ##print(f'end of {id_}')
    return False


def run() -> None:
    """Run program."""
    data = """2333133121414131402"""
    data_file = Path(__file__).absolute().parent / "day9.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    print("Running Part 1 (~57 seconds)...")

    blocks = list(expanded(data))

    start = perf_counter_ns()
    while needs_swap(blocks):
        perform_swap(blocks)
        ##print(''.join(str(char) if char is not None else '.' for char in blocks))
    checksum = calculate_fs_checksum(blocks)
    end = perf_counter_ns()
    print(f"Part 1 {checksum = }")
    print(f"Took {(end - start) / 1e9} seconds")

    print("Running Part 2 (~2 minutes and 20 seconds)...")

    blocks = list(expanded(data))
    ##print(''.join(str(char) if char is not None else '.' for char in blocks))

    cur_id = 9
    start = perf_counter_ns()
    while cur_id >= 0:
        if not block_swap(blocks, cur_id):
            cur_id -= 1
        ##else:
        ##    print(''.join(str(char) if char is not None else '.' for char in blocks))
    checksum = calculate_fs_checksum(blocks)
    end = perf_counter_ns()
    print(f"Part 2 {checksum = }")
    print(f"Took {(end - start) / 1e9} seconds")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
