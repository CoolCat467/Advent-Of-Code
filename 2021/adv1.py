#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 1 - https://adventofcode.com/2021/day/1

"""Goals:
1) How many measurements are larger than the previous measurement?
2) How many sums from a sliding window of 3 values greater then the
previous sum?.
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 1"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import math
from collections import deque


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv1.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    data = [int(x) for x in data]
    # Solve 1
    last = math.inf
    rsum = 0
    for value in data:
        if value > last:
            rsum += 1
        last = value
    print(rsum)
    # Solve 2
    rsum = 0
    last = math.inf
    window = deque([0, *data[:2]], 3)
    for cval in data[2:]:
        window.popleft()
        window.append(cval)
        value = sum(window)
        if value > last:
            rsum += 1
        last = value
    print(rsum)


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
