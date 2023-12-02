#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 10 - https://adventofcode.com/2021/day/10

"""Goals:
1) How many paths through this cave system are there that visit small caves at most once?
2) How many paths through this cave system are there? (now can go to small > 1 if only 1).
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 12"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from collections import Counter

import numpy as np


def get_all_paths(point_map):
    "Return all paths."  # noqa: D300
    found = set()

    def find_path(pos, current):
        next_ = [*current, pos]
        if pos == "end":
            found.add(tuple(next_))
            return
        for dest in point_map[pos]:
            if dest.isupper() or dest not in current:
                find_path(dest, next_)

    find_path("start", [])
    return tuple(found)


def get_all_paths_small2(point_map):
    "Return all paths."  # noqa: D300
    found = set()

    def find_path(pos, current):
        if pos == "start" and current:
            return
        next_ = [*current, pos]
        if pos == "end":
            found.add(tuple(next_))
            return
        counts = Counter(x for x in next_ if x.islower())
        has_smol = any(np.array(tuple(counts.values()), int) > 1)
        for dest in point_map[pos]:
            if not has_smol or dest.isupper() or dest not in current:
                find_path(dest, next_)

    find_path("start", [])
    return tuple(found)


def map_all_conn(point_map):
    "Make map have all possible starts and ends, not just hiding in end."  # noqa: D300
    data = point_map
    for end, values in tuple(point_map.items()):
        for start in values:
            if start not in data:
                data[start] = []
            if end not in data[start]:
                data[start].append(end)
            if start not in data[end]:
                data[end].append(start)
    for key, values in data.items():
        data[key] = sorted(values)
    return data


def get_map(lines):
    "Return map between points."  # noqa: D300
    data = {}
    for line in lines:
        start, end = line.split("-")
        if start not in data:
            data[start] = []
        data[start].append(end)
    return map_all_conn(data)


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv12.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    ##    data = """fs-end
    ##he-DX
    ##fs-he
    ##start-DX
    ##pj-DX
    ##end-zg
    ##zg-sl
    ##zg-pj
    ##pj-he
    ##RW-he
    ##fs-DX
    ##pj-RW
    ##zg-RW
    ##start-pj
    ##he-WI
    ##zg-he
    ##pj-fs
    ##start-RW""".splitlines()
    # Solve 1
    point_map = get_map(data)
    paths = get_all_paths(point_map)
    print(len(paths))
    # Solve 2
    paths = get_all_paths_small2(point_map)
    print(len(paths))


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
