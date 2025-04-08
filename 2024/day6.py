"""Advent of Code 2024 Day 6."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 6
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

__title__ = "Advent of Code 2024 Day 6"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from enum import IntEnum, auto
from pathlib import Path
from time import perf_counter_ns
from typing import TYPE_CHECKING, NamedTuple, Self

if TYPE_CHECKING:
    from collections.abc import Iterable


class Dir(IntEnum):
    """Direction."""

    up_down = 0
    left_right = auto()
    both = auto()


class Map(NamedTuple):
    """Map data."""

    size: tuple[int, int]
    guard_pos: tuple[int, int]
    guard_dir: int
    boxes: set[tuple[int, int]]

    @classmethod
    def load(cls, string: str) -> Self:
        """Load map from string."""
        lines = string.splitlines()
        height = len(lines)
        width = len(lines[0])

        guard_pos = (0, 0)
        guard_dir = 0

        boxes: list[tuple[int, int]] = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                # Blank, not important
                if char == ".":
                    continue
                # Box/object of some sort
                if char == "#":
                    boxes.append((x, y))
                    continue
                # Guard
                guard_pos = (x, y)
                if char == "^":
                    guard_dir = 0
                elif char == ">":
                    guard_dir = 1
                elif char == "v":
                    guard_dir = 2
                elif char == "<":
                    guard_dir = 3
                else:
                    raise ValueError(f"Unhandled character {char!r}")
        return cls(
            (width, height),
            guard_pos,
            guard_dir,
            set(boxes),
        )

    def map_tick(self) -> Self:
        """Return new map instance after performing tick."""
        x, y = self.guard_pos
        if self.guard_dir % 2 == 0:
            # Up down
            y += ((self.guard_dir >= 2) * 2) - 1
        else:
            x += 1 - ((self.guard_dir >= 2) * 2)

        next_ = (x, y)
        dir_ = self.guard_dir
        # If new position inside a box,
        if next_ in self.boxes:
            # go back to old position
            next_ = self.guard_pos
            # rotate 90 degrees
            dir_ = (dir_ + 1) % 4

        return self._replace(
            guard_pos=next_,
            guard_dir=dir_,
        )

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        """Return if given position is out of bounds."""
        w, h = self.size
        return (x < 0 or x >= w) or (y < 0 or y >= h)

    def guard_out_of_bounds(self) -> bool:
        """Return if guard position is out of bounds."""
        return self.is_out_of_bounds(*self.guard_pos)

    def get_guard_direction(self) -> Dir:
        """Return guard direction enum."""
        return Dir(self.guard_dir % 2)


def get_point_edges(
    x: int,
    y: int,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Return edges of given point."""
    return (
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    )


def get_intersection_edges(
    intersections: Iterable[tuple[int, int]],
) -> set[tuple[int, int]]:
    """Return set of all edges of all intersections."""
    points: set[tuple[int, int]] = set()
    for x, y in intersections:
        points.update(get_point_edges(x, y))
    return points


def run() -> None:
    """Run program."""
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    data_file = Path(__file__).absolute().parent / "day6.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Load map
    map_ = Map.load(data)

    unique_pos: set[tuple[int, int]] = set()
    pos_dirs: dict[tuple[int, int], Dir] = {}
    # Simulate movement until out of bounds
    while not map_.guard_out_of_bounds():
        # Remember current position
        unique_pos.add(map_.guard_pos)

        # Remember directions
        if map_.guard_pos not in pos_dirs:
            pos_dirs[map_.guard_pos] = map_.get_guard_direction()
        elif pos_dirs[map_.guard_pos] != map_.get_guard_direction():
            pos_dirs[map_.guard_pos] = Dir.both

        # Get next tick
        map_ = map_.map_tick()
    print(f"{len(unique_pos) = }")

    ##rows: set[int] = set()
    ##cols: set[int] = set()
    ##for (col, row), dir_ in pos_dirs.items():
    ##    if dir_ == Dir.both:
    ##        rows.add(row)
    ##        cols.add(col)
    ##    elif dir_ == Dir.left_right:
    ##        rows.add(row)
    ##    elif dir_ == Dir.up_down:
    ##        cols.add(col)
    ##intersections = {(x, y) for x in rows for y in cols}

    # brute force bad
    print("Will take around 1 minute and 27 seconds")
    max_ = round(len(unique_pos) * 1.5)

    valid = 0

    # Reload map
    map_ = Map.load(data)

    # Find possible place locations
    available_placements = unique_pos - map_.boxes - {map_.guard_pos}
    ##intersections = {pos for pos, dir_ in pos_dirs.items() if dir_ == Dir.both}
    ##available_placements &= get_intersection_edges(intersections)

    print(f"{len(available_placements) = }")

    start = perf_counter_ns()
    for x, y in available_placements:
        # Make copy with new box in it
        new_boxes = map_.boxes | {(x, y)}

        copy = map_._replace(boxes=new_boxes)

        seen_data: set[tuple[int, int, int]] = set()
        for _ in range(max_):
            pos_data = (*copy.guard_pos, copy.guard_dir)
            if pos_data not in seen_data:
                seen_data.add(pos_data)
            else:
                # Already been here, so looping!
                valid += 1
                break

            # If out of bounds, bad
            if copy.guard_out_of_bounds():
                break

            # Tick map
            copy = copy.map_tick()
        else:
            # If continued without hitting break
            valid += 1
    end = perf_counter_ns()
    print(f"{valid = }")
    print(f"{(end - start) / 1e9} seconds")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
