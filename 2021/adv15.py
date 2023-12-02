#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 15 - https://adventofcode.com/2021/day/15

"""Goals:
1)
2).
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 15"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import numpy as np


def main(grid):  # noqa: D103
    w, h = len(grid[0]), len(grid)
    risk = np.zeros((w, h), int)
    for y in range(h):
        for x in range(w):
            if x == 0 and y == 0:
                risk[y, x] = 0
            ##                risk[x, y] = 0
            else:
                risks = []
                if x > 0:
                    risks.append(risk[y, x - 1])
                ##                    risks.append(risk[x-1, y])
                if y > 0:
                    risks.append(risk[y - 1, x])
                ##                    risks.append(risk[x, y-1])
                ##                print(risks)
                risk[y, x] = min(risks) + grid[y][x]
    print(risk)
    return risk[h - 1, w - 1]


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv15.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    ##    data = """1163751742
    ##1381373672
    ##2136511328
    ##3694931569
    ##7463417111
    ##1319128137
    ##1359912421
    ##3125421639
    ##1293138521
    ##2311944581""".splitlines()
    # Process data
    ##    grid = Grid.read_lines(data)
    [list(map(int, line)) for line in data]


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
