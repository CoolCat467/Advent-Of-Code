#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 2 - https://adventofcode.com/2021/day/2

"""Goals:
1) What do you get if you multiply your final horizontal position by your final depth? (first bad)
2) What do you get if you multiply your final horizontal position by your final depth? (properly)
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 2'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from abc import ABC, abstractmethod

class SubmarineCommand(ABC):
    "Command for submarine"
    name = None
    def __init__(self, nargs=1):
        self.nargs = nargs
        self.data = []
        self.pos = {}
    
    @abstractmethod
    def apply(self):
        "Application of self"
    
    def read(self, input_, curpos):
        "Read input and return self.apply()"
        data = input_.split(' ')
        if data[0] != self.name:
            return None
        self.data = data[1:1+self.nargs]
        self.pos = curpos
        return self.apply()

class Forward1(SubmarineCommand):
    "Forward command"
    name = 'forward'
    def __init__(self):
        super().__init__(1)
    def apply(self):
        return {'x': int(self.data[0])}

class Down1(SubmarineCommand):
    "Down command"
    name = 'down'
    def __init__(self):
        super().__init__(1)
    def apply(self):
        return {'y': int(self.data[0])}

class Up1(SubmarineCommand):
    "Up command"
    name = 'up'
    def __init__(self):
        super().__init__(1)
    def apply(self):
        return {'y': -int(self.data[0])}

class SubmarineParser1:
    "Submarine parser, reads submarine commands and changes self.position from them"
    commands = [Forward1, Down1, Up1]
    init = {'x':0, 'y':0}
    def __init__(self):
        self.position = self.init
    
    def __repr__(self):
        return str(self.position)
    
    def parse(self, commands):
        "Parse commands and update position"
        for command in commands:
            for reader in self.commands:
                if reader.name == command.split(' ')[0]:
                    value = reader().read(command, self.position)
                    for key in value:
                        self.position[key] += value[key]

class Forward2(Forward1):
    "Proper forward command"
    def apply(self):
        x_pos = int(self.data[0])
        return {
            'x':x_pos,
            'y':self.pos['aim']*x_pos
        }

class Down2(Down1):
    "Proper down command"
    def apply(self):
        return {'aim':int(self.data[0])}

class Up2(Up1):
    "Proper up command"
    def apply(self):
        return {'aim':-int(self.data[0])}

# pylint: disable=R0903
class SubmarineParser2(SubmarineParser1):
    "Proper submarine parser"
    init = {'x':0, 'y':0, 'aim':0}
    commands = [Forward2, Down2, Up2]

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv2.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    # Solve 1
    submarine = SubmarineParser1()
    submarine.parse(data)
    print(submarine.position['x']*submarine.position['y'])
    # Solve 2
    submarine = SubmarineParser2()
    submarine.parse(data)
    print(submarine.position['x']*submarine.position['y'])

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
