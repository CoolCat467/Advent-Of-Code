#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 13 - https://adventofcode.com/2021/day/13

"""Goals:
1) How many dots are visible after completing just the first fold instruction on your transparent
paper?
2) What code do you use to activate the infrared thermal imaging camera system?
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 13'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import numpy as np

# pylint: disable=C0103

class Grid:
    "Grid object, represents transparent paper"
    def __init__(self):
        self.grid = np.array((0), int)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        lines = []
        for row in self.grid[:]:
            line = ''
            for x in row:
                line += ' #'[min(x, 1)]
            lines.append(line)
        return '\n'.join(lines)
    
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
    
    @classmethod
    def from_points(cls, points):
        "Read line data into internal grid"
        self = cls()
        w = max(p[0] for p in points)+1
        h = max(p[1] for p in points)+1
        self.grid = np.zeros((h, w), int)
        
        for x, y in points:
            self.grid[y, x] = 1
        return self
    
##    def fold_y(self, point):
##        "Fold across y = point."
##        fix = self.grid.shape[0]/2 == point
##        mirror = np.flipud(self.grid[point+fix:, :])
##        self.grid = self.grid[:point+(fix^1), :]
##        self.grid += mirror
##    
##    def fold_x(self, point):
##        "Fold across x = point."
##        fix = self.grid.shape[1]/2 == point
##        print(fix)
##        mirror = np.fliplr(self.grid[:, point+fix:])
##        self.grid = self.grid[:, :point-1]
##        self.grid += mirror
##    
##    def preform_folds(self, folds):
##        "Preform folds."
##        for type_, point in folds:
##            if type_ == 'x':
##                self.fold_x(int(point))
##            else:
##                self.fold_y(int(point))
##            if self.grid.shape[0] < 80:
##                print(self)
##            print('$'*16+f' {self.total_visible()}')
    
    def total_visible(self):
        "Return total number of visible points."
        return np.count_nonzero(self.grid)

class PointGrid:
    "Point Grid"
    def __init__(self):
        self.dim = (0, 0)
        self.points = []
    
    @classmethod
    def from_points(cls, points):
        "Read line data into internal grid"
        self = cls()
        w = max(p[0] for p in points)+1
        h = max(p[1] for p in points)+1
        
        self.dim = (w, h)
        self.points = points
        return self
    
    def fold_y(self, value):
        "Fold up"
        new = set()
        for point in self.points:
            x, y = point
            ny = 2*value-y if y > value else y
            val = (x, ny)
            new.add(val)
        self.points = list(new)
    
    def fold_x(self, value):
        "Fold left"
        new = set()
        for point in self.points:
            x, y = point
            nx = 2*value-x if x > value else x
            val = (nx, y)
            new.add(val)
        self.points = list(new)
    
    def preform_folds(self, folds):
        "Preform folds."
        for type_, point in folds:
            if type_ == 'x':
                self.fold_x(int(point))
            else:
                self.fold_y(int(point))
            print('$'*3+f' {self.total_visible()}')
##            if len(self.points) < 400:
        print(Grid.from_points(self.points))
    
    def total_visible(self):
        "Return total number of visible points."
        return len(self.points)

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv13.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read()
        rfile.close()
    # Prepare data
##    data = """6,10
##0,14
##9,10
##0,3
##10,4
##4,11
##6,0
##6,12
##4,1
##0,13
##10,12
##3,4
##3,0
##8,4
##1,10
##2,14
##8,10
##9,0
##
##fold along y=7
##fold along x=5"""
    points, instruct = data.split('\n\n')
    points = [tuple(map(int, p.split(','))) for p in points.splitlines()]
    instruct = [i.split('fold along ')[1].split('=') for i in instruct.splitlines()]
    # Solve 1 & 2
    grid = PointGrid.from_points(points)
    grid.preform_folds(instruct)
    print(grid.total_visible())    

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
