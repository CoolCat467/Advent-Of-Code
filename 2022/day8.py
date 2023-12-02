#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 7

"Advent of Code 2022 Day 7."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 7"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import io

import numpy as np


def to_grid(
    lines: list[str],
) -> np.ndarray[tuple[int, int], np.dtype[np.int0]]:
    "Convert lines into array."  # noqa: D300
    width = len(lines[0])
    height = len(lines)
    values: list[int] = sum(
        ([int(char) for char in line] for line in lines),
        start=[],
    )
    return np.array(values, dtype=np.int0).reshape((width, height))


def row_indexes(column: int, dims: int) -> list[int]:
    "Get row indexes from column."  # noqa: D300
    return list(range(column * dims, (column + 1) * dims))


def column_indexes(row: int, dims: int) -> list[int]:
    "Get column indexes from row."  # noqa: D300
    return list(range(row, dims * dims, dims))


def part_one(grid: np.ndarray[tuple[int, int], np.dtype[np.int0]]) -> int:
    "Calculate how many trees are visible from outside the grid."  # noqa: D300
    if grid.shape[0] != grid.shape[1]:
        raise ValueError("Unhandled case: width != height")
    width = grid.shape[0]
    elements = grid.shape[0] * grid.shape[1]
    hidden = set(range(elements))
    hidden -= set(range(width))
    hidden -= {i * width for i in range(width)}
    hidden -= {i * width - 1 for i in range(width)}
    hidden -= {i + (width * (width - 1)) for i in range(width)}

    for get_func in (row_indexes, column_indexes):
        for row_idx in range(width):
            base_row = get_func(row_idx, width)
            for row in (base_row, reversed(base_row)):
                last = np.int0(-1)
                for index in row:
                    value = grid.flat[index]
                    if last < value:
                        last = value
                        hidden.discard(index)
    return elements - len(hidden)


def part_two(grid: np.ndarray[tuple[int, int], np.dtype[np.int0]]) -> int:
    "Calculate the highest scenic score possible for any tree."  # noqa: D300
    if grid.shape[0] != grid.shape[1]:
        raise ValueError("Unhandled case: width != height")
    gwidth = grid.shape[0]
    gheight = grid.shape[1]

    cur_highest = 0
    for y in range(1, gheight - 1):
        for x in range(1, gwidth - 1):
            height = grid[y, x]
            total = 1

            see = 0
            for rx in reversed(range(x)):
                see += 1
                if grid[y, rx] >= height:
                    break
            total *= see

            see = 0
            for rx in range(1, gwidth - x):
                see += 1
                if grid[y, x + rx] >= height:
                    break
            total *= see

            see = 0
            for ry in reversed(range(y)):
                see += 1
                if grid[ry, x] >= height:
                    break
            total *= see

            see = 0
            for ry in range(1, gheight - y):
                see += 1
                if grid[y + ry, x] >= height:
                    break
            total *= see

            if total > cur_highest:
                cur_highest = total
    return cur_highest


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """30373
25512
65332
33549
35390"""

    file = io.StringIO(test_data)
    ##    file = open('day8.txt', encoding='utf-8')

    lines = file.read().splitlines()
    file.close()

    grid = to_grid(lines)

    print(f"{part_one(grid) = }")
    print(f"{part_two(grid) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
