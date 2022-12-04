#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of code 2021 day 6 - https://adventofcode.com/2021/day/6

"""Goals:
1) Model lantern fish for 80 days
2) Model lantern fish but now 256 days with > 1 trillion fish by last day.
"""

# Programmed by CoolCat467

__title__ = 'Advent of Code 2021 - Day 6'
__author__ = 'CoolCat467'
__version__ = '0.0.0'
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

class Fish:
    "Fish class remembering spawn delay, initial cooldown, and current state."
    __slots__ = ('delay', 'init', 'timer')
    def __init__(self, spawn_delay, init_cooldown, state):
        self.delay = spawn_delay
        self.init = init_cooldown
        self.timer = state
    
    def __str__(self):
        return str(self.timer)
    
    def tick(self):
        "Tick timer and return None if no new fish, or values to init new fish with."
        self.timer -= 1
        if self.timer >= 0:
            return None
        self.timer = self.delay
        return (self.delay, self.init, self.init+self.delay)

class FishSim:
    "Fish Simulation"
    def __init__(self, fish):
        self.fish = fish
    
    def create_fish(self, *args):
        "Make new fish"
        fish = Fish(*args)
        self.fish.append(fish)
    
    def tick(self):
        "Process all fish by one day and make new"
        to_create = []
        for fish in iter(self.fish):
            new = fish.tick()
            if new is None:
                continue
            to_create.append(new)
        for new in to_create:
            self.create_fish(*new)

# pylint: disable=R0903
class BetterFishSim:
    "Better fish simulation"
    __slots__ = ('delay', 'init_add', 'future')
    """Initial simulation is bad and can't handle trillions of fish in a realistic
ammount of time. Instead, just remember how many are going to hav spawn in a number
of days in the future. Then, for processing days, just pop zero, add value to
future day {delay}, and also add value to future day {delay+init}. After
all processed, shift future days by -1. To get total fish, get sum of fish
that will spawn in the future."""
    def __init__(self, delay, init, data):
        self.delay = delay
        self.init_add = init
        self.future = {x:0 for x in range(1, self.delay+self.init_add)}
        for timer in data:
            self.future[timer+1] = data.count(timer)
    
    def fish_after(self, days):
        "Return the number of fish that will exist with unlimited resources after n days."
        for _ in range(days):
            future = {k-1:v for k, v in self.future.items()}
            for day in range(self.delay+self.init_add+1):
                if not day in future:
                    future[day] = 0
            if not 0 in future:
                continue
            now = future[0]
            future[self.delay] += now
            future[self.delay+self.init_add] += now
            del future[0]
            self.future = future
##            print(', '.join(f'{k-1}: {v}' for k, v in future.items() if v > 0))
        return sum(future.values())

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv6.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().split(',')
        rfile.close()
##    data = "3,4,3,1,2".split(',')
    data = list(map(int, data))
    # Solve 1
####    print(f'Initial: {",".join(map(str, data))}')
##    fish = [Fish(6, 2, v) for v in data]
##    sim = FishSim(fish)
##    for day in range(80):
##        sim.tick()
####        print(",".join(map(str, sim.fish)))
##    print(len(sim.fish))
####        print(f'{day=}: {",".join(map(str, sim.fish))}')
    sim = BetterFishSim(7, 2, data)
    print(sim.fish_after(80))
    # Solve 2
    sim2 = BetterFishSim(7, 2, data)
    print(sim2.fish_after(256))
##        print(",".join(map(str, sim.fish)))

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
