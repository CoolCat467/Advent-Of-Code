#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 12

"Advent of Code 2022 Day 12."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 12"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import io
from collections import deque

import numpy as np


def to_grid(
    lines: list[str],
) -> tuple[np.ndarray[tuple[int, int], np.dtype[np.int0]], int, int]:
    "Convert lines into array."  # noqa: D300
    width = len(lines[0])
    height = len(lines)
    values: list[int] = []
    start = 0
    end = 0
    for line in lines:
        for char in line:
            if char == "S":
                start = len(values)
                values.append(0)
            elif char == "E":
                end = len(values)
                values.append(25)
            else:
                values.append(ord(char) - 97)  # - ord('a')
    return np.array(values, dtype=np.int0).reshape((width, height)), start, end


def pawn_move(index: int, row_size: int, item_cap: int) -> list[int]:
    "Get positions pawn can move in."  # noqa: D300
    y, x = divmod(index, row_size)
    indexes = ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1))
    value = [y * row_size + x for x, y in indexes]
    return [v for v in value if 0 < v < item_cap]


def part_one(
    grid: np.ndarray[tuple[int, int], np.dtype[np.int0]],
    start: int,
    end: int,
) -> int:
    "Find length of shortest path from start to end."  # noqa: D300
    visited: set[int] = set()
    width, height = grid.shape
    item_cap = width * height

    paths: dict[int, int] = {start: 0}

    unhandled: deque[int] = deque((start,))
    while unhandled:
        point = unhandled.popleft()
        reachable = grid.flat[point] + 1
        to_here = paths[point] + 1

        visit = set(pawn_move(point, width, item_cap)) - visited
        for new in visit:
            if grid.flat[new] > reachable:
                continue
            paths[new] = min(paths.get(new, to_here), to_here)
            if new not in unhandled and new not in visited:
                unhandled.append(new)

            visited.add(point)
    return paths[end]


def part_two(
    grid: np.ndarray[tuple[int, int], np.dtype[np.int0]],
    start: int,
    end: int,
) -> int:
    "Find length of shortest path that starts at lowest elevation to end."  # noqa: D300
    visited: set[int] = set()
    width, height = grid.shape
    item_cap = width * height

    unhandled: deque[int] = deque(
        (idx for idx, v in enumerate(grid.flat) if v == 0),
    )
    paths: dict[int, int] = dict.fromkeys(unhandled, 0)

    while unhandled:
        point = unhandled.popleft()
        reachable = grid.flat[point] + 1
        to_here = paths[point] + 1

        visit = set(pawn_move(point, width, item_cap)) - visited
        for new in visit:
            if grid.flat[new] > reachable:
                continue
            paths[new] = min(paths.get(new, to_here), to_here)
            if new not in unhandled and new not in visited:
                unhandled.append(new)

            visited.add(point)
    return paths[end]


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    file = io.StringIO(test_data)
    ##    file = open('day12.txt', encoding='utf-8')

    lines = file.read().splitlines()
    file.close()

    grid, start, end = to_grid(lines)

    print(f"{part_one(grid, start, end) = }")
    print(f"{part_two(grid, start, end) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
