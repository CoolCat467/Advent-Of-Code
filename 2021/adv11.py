#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 11 - https://adventofcode.com/2021/day/11

"""Goals:
1) How many total flashes are there after 100 steps?
2) How many iterations until synchronized?.
"""  # noqa: D205

# Programmed by CoolCat467

# pylint: disable=C0103

__title__ = "Advent of Code 2021 - Day 11"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from collections import deque

import numpy as np


class Grid:
    "Grid object, represents octopus grid."  # noqa: D300

    def __init__(self):  # noqa: D107
        self.grid = np.array((0), int)

    def __repr__(self):  # noqa: D105
        return str(self.grid)

    def set_pos(self, x, y, value):
        "Set value at x, y to value."  # noqa: D300
        self.grid[x, y] = value

    def get_pos(self, x, y):
        "Return value at position."  # noqa: D300
        return self.grid[x, y]

    def point_valid(self, x, y):
        "Return if x, y is valid point."  # noqa: D300
        w, h = self.grid.shape
        return not (x < 0 or x >= w or y < 0 or y >= h)

    @staticmethod
    def get_sides(cx, cy):
        "Return sides of point at cx, cy."  # noqa: D300
        return (
            (cx - 1, cy - 1),
            (cx - 1, cy),
            (cx - 1, cy + 1),
            (cx, cy - 1),
            (cx, cy + 1),
            (cx + 1, cy - 1),
            (cx + 1, cy),
            (cx + 1, cy + 1),
        )

    def only_valid(self, points):
        "Out of points, only return valid points."  # noqa: D300
        valid = []
        for x, y in points:
            if self.point_valid(x, y):
                valid.append((x, y))
        return valid

    def circle_points(self, cx, cy):
        "Return valid points circleing cx, cy."  # noqa: D300
        return self.only_valid(self.get_sides(cx, cy))

    def get_circle(self, cx, cy):
        "Return point at cx, cy, and all other valid points immediately surrounding it."  # noqa: D300
        values = [self.get_pos(x, y) for x, y in self.circle_points(cx, cy)]
        return self.get_pos(cx, cy), values

    @classmethod
    def read_lines(cls, lines):
        "Read line data into internal grid."  # noqa: D300
        self = cls()
        w, h = len(lines[0]), len(lines)
        self.grid = np.zeros((h, w), int)

        for x in range(w):
            for y in range(h):
                self.set_pos(x, y, int(lines[x][y]))
        return self

    def step(self):
        "Step simulation by 1."  # noqa: D300
        self.grid += 1
        ##        flash = self.grid > 9
        ##        print(flash)
        over = np.where(self.grid > 9)
        flashes = deque(zip(*over))
        processed = set(flashes)
        flashed = 0
        while flashes:
            x, y = flashes.pop()
            surround = (
                value
                for value in self.circle_points(x, y)
                if value not in processed
            )
            for px, py in surround:
                self.grid[px, py] += 1
                if self.grid[px, py] > 9:
                    flashes.append((px, py))
                    processed.add((px, py))
            flashed += 1
            self.set_pos(x, y, 0)
        ##        print(self.grid > 9)
        return flashed

    def check_sync(self):
        "Check if all octopus are synchronized."  # noqa: D300
        return np.all(self.grid == self.grid[0, 0])

    def steps(self, count):
        "Perform count steps."  # noqa: D300
        flashes = 0
        for _ in range(count):
            flashes += self.step()
        self.check_sync()
        return flashes

    def sync_all(self):
        "Return number of steps required to sync all."  # noqa: D300
        steps = 0
        while not self.check_sync():
            self.step()
            steps += 1
        return steps


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv11.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    ##    data = """5483143223
    ##2745854711
    ##5264556173
    ##6141336146
    ##6357385478
    ##4167524645
    ##2176841721
    ##6882881134
    ##4846848554
    ##5283751526""".splitlines()
    ##    data = """11111
    ##19991
    ##19191
    ##19991
    ##11111""".splitlines()
    # Solve 1
    grid = Grid.read_lines(data)
    ##    grid.steps(100)
    ##    print(grid)
    print(grid.steps(100))
    ##    print(grid)
    # Solve 2
    grid = Grid.read_lines(data)
    print(grid.sync_all())


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
