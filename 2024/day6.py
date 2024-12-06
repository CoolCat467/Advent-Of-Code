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


from collections import Counter
from enum import IntEnum, auto
from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple, Self


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
                if char == ".":
                    continue
                if char == "#":
                    boxes.append((x, y))
                    continue
                if char == "^":
                    guard_pos = (x, y)
                    guard_dir = 0
                if char == ">":
                    guard_pos = (x, y)
                    guard_dir = 1
                if char == "v":
                    guard_pos = (x, y)
                    guard_dir = 2
                if char == "<":
                    guard_pos = (x, y)
                    guard_dir = 3
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
        if next_ in self.boxes:
            next_ = self.guard_pos
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
    data = Path("day6.txt").read_text()
    map_ = Map.load(data)
    unique_pos: set[tuple[int, int]] = set()
    pos_dirs: dict[tuple[int, int], Dir] = {}
    unique_pos_count: Counter[tuple[int, int]] = Counter()
    while not map_.guard_out_of_bounds():
        unique_pos.add(map_.guard_pos)
        unique_pos_count[map_.guard_pos] += 1
        if map_.guard_pos not in pos_dirs:
            pos_dirs[map_.guard_pos] = map_.get_guard_direction()
        elif pos_dirs[map_.guard_pos] != map_.get_guard_direction():
            pos_dirs[map_.guard_pos] = Dir.both
        map_ = map_.map_tick()
    print(f"{len(unique_pos) = }")

    # brute force bad
    print("Will take around 1 minute and 27 seconds")
    max_ = round(len(unique_pos) * 1.5)
    valid = 0
    map_ = Map.load(data)
    start = perf_counter_ns()
    for x, y in unique_pos - map_.boxes:
        if map_.guard_pos == (x, y):
            continue
        ##prev_dir_at_box = pos_dirs[(x, y)]
        # Make copy with new box in it
        new_boxes = map_.boxes | {(x, y)}

        ##guard_pos = map_.guard_pos
        ##guard_dir = map_.guard_dir

        ##    # Go to last position at this position
        ##    nx, ny = x, y
        ##    if map_.guard_dir % 2 == 0:
        ##        # Up down
        ##        ny -= ((map_.guard_dir >= 2) * 2) - 1
        ##    else:
        ##        nx -= 1 - ((map_.guard_dir >= 2) * 2)
        ##    guard_dir = prev_dir_at_box
        ##    guard_pos = (nx, ny)
        copy = map_._replace(boxes=new_boxes)
        # , guard_pos=guard_pos, guard_dir=guard_dir)
        ##unique_pos_count_copy: Counter[tuple[int, int]] = Counter()
        ##same = 0
        for _ in range(max_):
            if copy.guard_out_of_bounds():
                break
            ##unique_pos_count_copy[map_.guard_pos] += 1
            ##prev_dir_here = pos_dirs.get(copy.guard_pos)
            ##if (
            ##    prev_dir_here is not None
            ##    and (
            ##        prev_dir_here == Dir.both
            ##        or prev_dir_here == copy.get_guard_direction()
            ##    )
            ##    and (
            ##        unique_pos_count_copy[map_.guard_pos]
            ##        > unique_pos_count[map_.guard_pos]
            ##    )
            ##):
            ##    # Been here before facing same direction
            ##    same += 1
            ##if same > (len(unique_pos) // 2):
            ##    valid += 1
            ##    break
            copy = copy.map_tick()
        else:
            # If continued without hitting break
            valid += 1
            ##print(f'{same = }')
    end = perf_counter_ns()
    print(f"{valid = }")
    print(f"{(end - start) / 1e9} seconds")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
