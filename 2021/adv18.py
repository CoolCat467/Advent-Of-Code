#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 18 - https://adventofcode.com/2021/day/18

"""Goals:
1) 
2) 
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 18'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import json
from vector import Vector
import math

def to_vec(lists):
    def step(item):
        x, y = item
        if isinstance(x, int) and isinstance(y, int):
            return Vector(x, y)
        items = []
        for val in item:
            if isinstance(val, int):
                items.append(val)
            else:
                items.append(step(val))
        return Vector.from_iter(items)
    return step(lists)

def explode_number(snail_num):
    "Explode snail number"
    def step(items, nest):
        value = []
        for idx, val in enumerate(items):
            if not isinstance(val, int):
                if nest < 3:
                    val = step(val, nest+1)
                    value.append(val)
                else:
                    comb = items[idx^1]
                    comb = Vector.from_iter(([0]*(idx^1))+[comb]+([0]*idx))
                    res = list(Vector.from_iter(val) + comb)
                    right = res[idx] if idx == 1 else None
                    left = res[idx] if idx == 0 else None
                    res[idx] = 0
                    return res, right, left
            else:
                value.append(val)
        return value
    result = step(snail_num, 0)
    def fix_right(items, right=None, left=None):
        values = []
        frm = None
        for idx, val in enumerate(items):
            if isinstance(val, tuple):
                val, right, left = val
                frm = idx
            elif not isinstance(val, int):
                val, right, left = fix_right(val, right, left)
            values.append(val)
        if frm is None:
            if not right is None:
                if isinstance(values[1], int):
                    values[1] += right
                    right = None
            if not left is None:
                if isinstance(values[0], int):
                    values[0] += left
                    left = None
        return values, right, left
##    print(result)
    return fix_right(result)[0]

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv18.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().splitlines()
        rfile.close()
##    data = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
##[[[5,[2,8]],4],[5,[[9,9],0]]]
##[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
##[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
##[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
##[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
##[[[[5,4],[7,7]],8],[[8,3],8]]
##[[9,3],[[9,9],[6,[4,9]]]]
##[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
##[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()
    # Process data
    data = [json.loads(line) for line in data]
##    print(data)
##    data = [to_vec(item) for item in data]
    # Solve 1
    

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
