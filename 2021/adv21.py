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

def deterministic():
    x = 1
    while True:
        yield x
        x = (x%100)+1

class Player:
    def __init__(self, start_pos, dice):
        self.pos = start_pos
        self.dice = dice
        self.score = 0
    
    def __repr__(self):
        return f'<Player pos: {self.pos} score: {self.score}>'
    
    def roll(self):
        rolls = []
        for i in range(3):
            rolls.append(next(self.dice))
        self.pos = ((self.pos-1+sum(rolls))%10)+1
        self.score += self.pos
        return self.score

def simulate_deterministic(initials):
    dice = deterministic()
    players = [Player(x, dice) for x in initials]
    rolls = 0
    while True:
        for p_no, p in enumerate(players):
            rolls += 1
            if p.roll() >= 1000:
##                print(players)
##                print(f'{rolls*3=}')
##                return p_no+1
                return players[(p_no+1)%len(players)].score*(rolls*3)

class QuantumPlayer:
    __slots__ = ('num', 'score', 'pos')
    def __init__(self, num, pos, score=0):
        self.num = num
        self.pos = pos
        self.score = score
    
    def __repr__(self):
        return f'<QP pos: {self.pos} score: {self.score}>'

def simulate_dirac(initials):
    universes = deque([[QuantumPlayer(n, p) for n, p in enumerate(initials)]])
    wins = [0]*len(initials)
    while universes:
        players = universes.popleft()
        new_players = []
        for player in players:
            win = False
            rolls = [3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9]
            for x in rolls:
                pos = (player.pos+x)%9
                score = player.score + pos + 1
                if score >= 21:
                    win = True
                    break
                else:
                    new_players.append(QuantumPlayer(player.num, pos, score))
            if win:
                wins[player.num] += 1
                break
        if not win:
            universes.append(new_players)
    return wins

def run():
    "Solve problems"
    # Read file
    data = []
    with open('adv21.txt', 'r', encoding='utf-8') as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    data = [int(x.split(': ')[1]) for x in data]
    # Process data
    print(simulate_deterministic(data))
    # Solve 1
    print(simulate_dirac(data))
    # Solve 2
    

if __name__ == '__main__':
    print(f'{__title__} v{__version__}\nProgrammed by {__author__}.')
    run()
