#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 17 - https://adventofcode.com/2021/day/17

"""Goals:
1) What is the highest y position it reaches on this trajectory?
2) How many distinct initial velocity values cause the probe to be within the target area after any
step?
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 17'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import math
from vector import Vector

class Probe:
    "Probe object"
    def __init__(self, speed_x=0, speed_y=0):
        self.position = Vector(0, 0)
        self.speed = Vector(speed_x, speed_y)
        self.max_height = -math.inf
    
    def __repr__(self):
        return f'<Probe at {self.position}, speed {self.speed}>'
    
    def tick(self):
        "Move one step in simulation"
        self.position += self.speed
        self.max_height = max(self.max_height, self.position[1])
        sp_x = self.speed[0]
        newx = sp_x / abs(sp_x) if abs(sp_x) > 0 else 0
        self.speed -= (newx, 1)

class ProbeSim:
    "Probe simulation"
    def __init__(self, data):
        self.target = data
        self.cprobe = None
        self.targets = [Vector(self.target['x'][i], self.target['y'][i]) for i in range(2)]
        self.target_pos = sum(self.targets)/2
    
    def test_position(self):
        "See if current probe is in the right place"
        pos_x, pos_y = self.cprobe.position
        xmin, xmax = self.target['x']
        if pos_x < xmin or pos_x > xmax:
            return False
        ymin, ymax = self.target['y']
        if pos_y < ymin or pos_y > ymax:
            return False
        return True
    
    def test_path(self, speed_x, speed_y):
        "Test path with speed of speed_x, speed_y"
        self.cprobe = Probe(speed_x, speed_y)
        while True:
            pos_x, pos_y = self.cprobe.position
            max_x = self.targets[1][0]
            min_y = self.targets[0][1]
            if not (pos_x <= max_x and pos_y >= min_y):
                break
            self.cprobe.tick()
            if self.test_position():
                return True
        return False
    
    def find_max_y(self):
        "Find launch values and number of good ones"
        count = 0
        y_vals = {}
        min_y = self.targets[0][1]
        max_x = self.targets[1][0]
        for s_x in range(max_x, 0, -1):
            for s_y in range(min_y, -min_y):
                if self.test_path(s_x, s_y):
                    max_y = self.cprobe.max_height
                    y_vals[max_y] = (s_x, s_y)
                    count += 1
        return y_vals, count

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv17.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().strip()
        rfile.close()
##    data = 'target area: x=20..30, y=-10..-5'
    # Process data
    data = data.split('target area: ')[1].split(', ')
    target = {}
    for value in data:
        attr, val = value.split('=')
        target[attr] = tuple(map(int, val.split('..')))
    
    # Solve 1
    sim = ProbeSim(target)
    y_vals, count = sim.find_max_y()
    print(max(y_vals))
    # Solve 2
    print(count)
##    print(min(y_vals))

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
