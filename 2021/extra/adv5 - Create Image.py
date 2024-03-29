#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 5 - https://adventofcode.com/2021/day/5

"""Goals:
1) At how many points do at least two lines overlap? (Only horizontal & vertical)
2).
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 5"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import math

import numpy as np
import pygame
from vector import Vector


class Grid:  # noqa: D101
    def __init__(self):  # noqa: D107
        self.grid = np.zeros((1000, 1000), dtype=int)

    def __str__(self):  # noqa: D105
        return str("".join(self.grid[:]))

    def vent_point(self, x, y):
        "Add point as vent stream."  # noqa: D300
        tx = int(x)
        ty = int(y)
        self.grid[ty, tx] += 1

    def line(self, start, end):
        "Add vent points for a line."  # noqa: D300
        vector = end - start
        direction = vector.copy().normalize()
        angle = math.degrees(vector.get_heading())
        maxmag = max(start.magnitude, end.magnitude)
        add = []
        if angle % 90 == 0:
            add.append(tuple(start))
            for i in range(1, math.ceil(vector.magnitude) + 1):
                point = start + tuple(map(math.ceil, direction * [i, i]))
                point = Vector(*map(math.ceil, point))
                if point.magnitude <= maxmag and tuple(point) not in add:
                    add.append(tuple(point))
        else:
            angle = int(angle)
            for i in range(math.ceil(vector.magnitude / math.sqrt(2)) + 1):
                if angle == 45:
                    add.append((*start, i, i))
                elif angle == -45:
                    add.append(start - (-i, i))
                elif angle == 135:
                    add.append((*start, -i, i))
                elif angle == -135:
                    add.append(start - (i, i))
        for point in add:
            self.vent_point(*point)

    def read_lines(self, lines, non_slope=True):
        "Read vectors from file line data and add points to grid."  # noqa: D300
        for line in lines:
            parts = line.split(" -> ")
            start = Vector(*map(int, parts[0].split(",")))
            end = Vector(*map(int, parts[1].split(",")))
            if not non_slope and 0 not in start - end:
                continue
            self.line(start, end)

    def get_overlap_count(self):
        "Return number of points where at least two vents overlap."  # noqa: D300
        return (self.grid > 1).sum()

    def create_surf(self, colors):
        "Return surface from self."  # noqa: D300
        w, h = self.grid.shape
        surf = pygame.surface.Surface((w, h))
        surf.set_alpha(0)
        surf.unlock()
        for y in range(h):
            for x in range(w):
                value = self.grid[x, y]
                index = min(value, len(colors))
                ##                print((*colors[index], (value==0)*255))
                ##                color = pygame.color.Color(*colors[index])#a=(value!=0)*255)
                surf.set_at((x, y), [*list(colors[index]), (value != 0) * 255])
        ##                if value >0:
        ##                    print(color)
        ##                    print(surf.get_at((x, y)))
        surf.lock()
        return surf


def run():
    "Solve problems."  # noqa: D300
    # read file
    data = []
    with open("adv5.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    ##    data = """0,9 -> 5,9
    ##8,0 -> 0,8
    ##9,4 -> 3,4
    ##2,2 -> 2,1
    ##7,0 -> 7,4
    ##6,4 -> 2,0
    ##0,9 -> 2,9
    ##3,4 -> 1,4
    ##0,0 -> 8,8
    ##5,5 -> 8,2""".splitlines()
    ##    data = """1,1 -> 3,3
    ##9,7 -> 7,9""".splitlines()
    # Solve 1
    grid = Grid()
    grid.read_lines(data, False)
    ##    print(grid.grid[0:12, 0:12])
    print(grid.get_overlap_count())
    # Solve 2
    grid = Grid()
    grid.read_lines(data)
    print(grid.get_overlap_count())
    colors = (
        (0, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 0, 0),
        (255, 255, 0),
        (255, 0, 255),
        (255, 255, 255),
    )
    surface = grid.create_surf(colors).copy()
    pygame.image.save(surface, "Solution.png")


##    print(grid.grid[0:12, 0:12])


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    pygame.init()
    try:
        run()
    finally:
        pygame.quit()
