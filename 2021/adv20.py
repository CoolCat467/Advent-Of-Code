#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 20 - https://adventofcode.com/2021/day/20

"""Goals:
1) 
2) 
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 20'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from collections import deque
import numpy as np

class Grid:
    "Grid object, represents octopus grid"
    def __init__(self):
        self.grid = np.array((0), int)
    
    def __repr__(self):
        return str(self.grid)
    
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
        return ((cx-1, cy-1),
                (cx-1, cy),
                (cx-1, cy+1),
                (cx, cy-1),
                (cx, cy+1),
                (cx+1, cy-1),
                (cx+1, cy),
                (cx+1, cy+1))
    
    def only_valid(self, points):
        "Out of points, only return valid points."
        valid = []
        for x, y in points:
            if self.point_valid(x, y):
                valid.append((x, y))
        return valid
    
    def circle_points(self, cx, cy):
        "Return valid points circleing cx, cy."
        return self.only_valid(self.get_sides(cx, cy))
    
    def get_circle(self, cx, cy):
        "Return point at cx, cy, and all other valid points immidiately surrounding it."
        values = [self.get_pos(x, y) for x, y in self.circle_points(cx, cy)]
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
    
    

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv20.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    # Process data
    print(data)
    # Solve 1
    
    # Solve 2
    

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
