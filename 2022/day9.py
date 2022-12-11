#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022 Day 9

"Advent of Code 2022 Day 9"

# Programmed by CoolCat467

__title__ = 'Advent of Code 2022 Day 9'
__author__ = 'CoolCat467'
__version__ = '0.0.0'

from typing import Iterable, Iterator, Final

import io
import dataclasses


SHOW_STEP: Final = True


@dataclasses.dataclass(slots=True)
class Point:
    "Represents one two dimensional point"
    x: int
    y: int
    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y))

    def __add__(self, obj: Iterable[int]) -> 'Point':
        gen = iter(obj)
        return Point(self.x + next(gen), self.y + next(gen))

    def __iadd__(self, obj: Iterable[int]) -> 'Point':
        gen = iter(obj)
        self.x += next(gen)
        self.y += next(gen)
        return self

    def __sub__(self, obj: Iterable[int]) -> 'Point':
        gen = iter(obj)
        return Point(self.x - next(gen), self.y - next(gen))

    def __copy__(self) -> 'Point':
        return Point(self.x, self.y)

    copy = __copy__


class RopeSim:
    "Single length rope simulation"
    __slots__ = ('head', 'tail', 'visited')
    def __init__(self) -> None:
        self.head = Point(0, 0)
        self.tail = Point(0, 0)
        self.visited: set[tuple[int, int]] = {(0, 0)}

    def set_tail(self, point: Point) -> None:
        "Set tail and mark point as visited"
##        self.visited.add(point.x * 3 + point.y * 5)
        self.visited.add((point.x, point.y))
        self.tail = point

    def step(self, direction: str, count: int) -> None:
        "Preform one step of the simulation"
        dx = {'R': 1, 'L': -1}.get(direction, 0)
        dy = {'U': 1, 'D': -1}.get(direction, 0)
        delta = Point(dx, dy)
        for _ in range(count):
            prev_head = self.head.copy()
            self.head += delta

            x, y = self.head - self.tail
            if abs(x) > 1 or abs(y) > 1:
                self.set_tail(prev_head)


def copysign(x: int, y: int) -> int:
    "Copy sign of y to x"
    abs_x = abs(x)
    if y < 0:
        return -abs_x
    if y == 0:
        return x
    return abs_x


class RopeSimLong:
    "Rope simulation of longer rope (1 does not work properly)"
    __slots__ = ('length', 'stack', 'visited')
    def __init__(self, length: int) -> None:
        self.length = length
        self.stack = {i:Point(0, 0) for i in range(length+1)}
        self.visited: set[tuple[int, int]] = {(0, 0)}

    def set_tail(self, index: int, point: Point) -> None:
        "Mark point as visited"
        if index == self.length-1:
            self.visited.add((point.x, point.y))
        self.stack[index] = point
        if SHOW_STEP:
            self.show_map()

    def step(self, direction: str, count: int) -> None:
        "Preform one step"
        dx = {'R': 1, 'L': -1}.get(direction, 0)
        dy = {'U': 1, 'D': -1}.get(direction, 0)
        delta = Point(dx, dy)
        for _ in range(count):
            self.stack[0] += delta
            for idx in range(1, self.length):
                head = self.stack[idx-1]
                tail = self.stack[idx]

                dx, dy = head - tail
                if abs(dx) > 1 or abs(dy) > 1:
                    if abs(dx) > 1:
                        dx = copysign(abs(dx)-1, dx)
                    if abs(dy) > 1:
                        dy = copysign(abs(dy)-1, dy)
                    self.set_tail(idx, tail + (dx, dy))

    def show_map(self) -> None:
        "Show the current map"
        rev_stack = {tuple(v):k for k, v in self.stack.items()}
        # Find min and max of view port
        stack = set(rev_stack)
        points = self.visited | stack
        minmax = [[0, 0], [0, 0]]
        for point in points:
            values = tuple(point)
            for i in range(2):
                if values[i] < minmax[i][0]:
                    minmax[i][0] = values[i]
                if values[i] > minmax[i][1]:
                    minmax[i][1] = values[i]
        minx, maxx = minmax[0]
        miny, maxy = minmax[1]
        # Only do one print call to speed it up
        lines = ''
        # Need to flip y axis
        for y in reversed(range(miny-1, maxy+2)):
            for x in range(minx-1, maxx+2):
                if (x, y) in self.visited:
                    if x == 0 and y == 0:
                        lines += 's'
                        continue
                    lines += '#'
                    continue
                if (x, y) in stack:
                    item = rev_stack[(x, y)]
                    if item == 0:
                        lines += 'H'
                        continue
                    lines += str(item)
                    continue
                lines += '.'
            lines += '\n'
        print(lines)


def part_one(commands: list[tuple[str, int]]) -> int:
    "Calculate how many positions the tail of the rope visits at least once"
    sim = RopeSim()
    for direction, count in commands:
        sim.step(direction, count)
    return len(sim.visited)


def part_two(commands: list[tuple[str, int]]) -> int:
    "Calculate how many positions the tail of the rope visits at least once"
    sim = RopeSimLong(10)
    for direction, count in commands:
        sim.step(direction, count)
    return len(sim.visited)



def run() -> None:
    "Synchronous entry point"
    if not SHOW_STEP:
        print("Hey try turning SHOW_STEP to True it's cool\n")
##    test_data = """R 4
##U 4
##L 3
##D 1
##R 4
##D 1
##L 5
##R 2"""
    test_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    instructions: list[tuple[str, int]] = []

    file = io.StringIO(test_data)
##    file = open('day9.txt', encoding='utf-8')

    for line in file:
        command, spaces = line.split(' ', 1)
        instructions.append((command, int(spaces)))

    file.close()

    print(f'{part_one(instructions) = }')
    print(f'{part_two(instructions) = }')


if __name__ == '__main__':
    print(f'{__title__}\nProgrammed by {__author__}.\n')
    run()
