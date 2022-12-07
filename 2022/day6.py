#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022 Day 6

"Advent of Code 2022 Day 6"

# Programmed by CoolCat467

__title__ = 'Advent of Code 2022 Day 6'
__author__ = 'CoolCat467'
__version__ = '0.0.0'


import io
from collections import deque

##def slide_window_find(string: str, find: str) -> int | None:
##    "Return index of sliding window search for {find} in string"
##    size = len(find)
##    window = deque(string[:size], size)
##    for idx, char in enumerate(string[size:]):
##        if ''.join(window) == find:
##            return idx+size
##        window.append(char)
##    return None


def part_one(buffer: str) -> int | None:
    "Find start of packet"
    window = deque(buffer[:4], 4)
    for idx, char in enumerate(buffer[4:]):
        if len(set(window)) == 4:
            return idx+4
        window.append(char)
    return None


def part_two(buffer: str) -> int | None:
    "Find start of message packet"
    start = part_one(buffer)  # Find start of packet
    if start is None:
        return None
    window = deque(buffer[start:start+14], 14)
    for idx, char in enumerate(buffer[start+14:]):
        if len(set(window)) == 14:
            return idx+14+start
        window.append(char)
    return None


def run() -> None:
    "Synchronous entry point"
    test_data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

    file = io.StringIO(test_data)
##    file = open('day6.txt', encoding='utf-8')

    buffer = file.readline()
    file.close()

##    print(f'{buffer = }')

    print(f'{part_one(buffer) = }')
    print(f'{part_two(buffer) = }')


if __name__ == '__main__':
    print(f'{__title__}\nProgrammed by {__author__}.\n')
    run()
