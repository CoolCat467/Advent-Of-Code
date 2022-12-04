#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 9 - https://adventofcode.com/2021/day/9

"""Goals:
1) What is the sum of the risk levels of all low points on your heightmap?
2) What do you get if you multiply together the sizes of the three largest basins?
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 9'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from functools import reduce
import numpy as np

# pylint: disable=C0103

class Grid:
    "Grid object, represents sea floor height map"
    def __init__(self):
        self.grid = np.array((0), int)
    
    def set_pos(self, x, y, value):
        "Set value at x, y to value."
        self.grid[x, y] = value
    
    def get_pos(self, x, y):
        "Return value at position"
        return self.grid[x, y]
    
    def point_valid(self, x, y):
        "Return if x, y is valid point."
        w, h = self.grid.shape
        return not (x < 0 or x >= w or y < 0 or y >= h)
    
    @staticmethod
    def get_sides(cx, cy):
        "Return sides of point at cx, cy."
        return ((cx-1, cy),
                (cx, cy-1),
                (cx, cy+1),
                (cx+1, cy))
    
    def only_valid(self, points):
        "Out of points, only return valid points."
        valid = []
        for x, y in points:
            if self.point_valid(x, y):
                valid.append((x, y))
        return valid
    
    def get_plus(self, cx, cy):
        "Return point at cx, cy, and all other valid points immidiately touching it."
        values = [self.get_pos(x, y) for x, y in self.only_valid(self.get_sides(cx, cy))]
        return self.get_pos(cx, cy), values
    
    @classmethod
    def read_lines(cls, lines):
        "Read line data into internal grid"
        self = cls()
        w, h = len(lines[0]), len(lines)
        self.grid = np.zeros((h, w), int)
        
        for x in range(w):
            for y in range(h):
                self.set_pos(x, y, int(lines[x][y]))
        return self
    
    def get_low_points(self):
        "Return low points"
        lows = []
        w, h = self.grid.shape
        for x in range(w):
            for y in range(h):
                point, surround = self.get_plus(x, y)
                if all(point < s for s in surround):
                    lows.append((x, y))
        return lows
    
    def get_basins(self):
        "Get basins"
        lows = self.get_low_points()
        basins = []
        for low in lows:
            checked = [low]
            to_eval = [low]
            size = 1
            while to_eval:
                point = to_eval.pop()
                point_value = self.get_pos(*point)
                sides = self.get_sides(*point)
                sides = self.only_valid(s for s in sides if not s in checked)
                for x, y in sides:
                    side_value = self.get_pos(x, y)
                    if side_value > point_value and side_value != 9:
                        size += 1
                        to_eval.append((x, y))
                        checked.append((x, y))
            basins.append(checked)
        return basins

def run():
    "Solve problems"
    # read file
    data = []
    with open('adv9.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().splitlines()
        rfile.close()
##    data = """2199943210
##3987894921
##9856789892
##8767896789
##9899965678""".splitlines()
    # Solve 1
    grid = Grid.read_lines(data)
    low = grid.get_low_points()
    heights = [grid.get_pos(x,y) for x,y in low]
    risks = tuple(map(lambda x:x+1, heights))
    print(sum(risks))
    # Solve 2
    basins = grid.get_basins()
    basin_sizes = sorted((len(basin) for basin in basins), reverse=True)
    print(reduce(lambda x,y:x*y, basin_sizes[:3]))

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
