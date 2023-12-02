#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 4

"Advent of Code 2022 Day 4."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 4"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import io
from typing import cast


def section_to_range(pair: str) -> range:
    "Convert section to range."  # noqa: D300
    start, end = map(int, pair.split("-", 1))
    return range(start, end + 1)


def part_one(pairs: list[tuple[str, str]]) -> int:
    "Get total number of subsets from pairs."  # noqa: D300
    total_subset = 0
    for one, two in pairs:
        set_one = set(section_to_range(one))
        set_two = set(section_to_range(two))
        if set_one.issubset(set_two) or set_two.issubset(set_one):
            total_subset += 1
    return total_subset


def part_two(pairs: list[tuple[str, str]]) -> int:
    "Get total number of intersecting pairs."  # noqa: D300
    total = 0
    for one, two in pairs:
        set_one = set(section_to_range(one))
        set_two = set(section_to_range(two))
        if set_one & set_two:
            total += 1
    return total


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    file = io.StringIO(test_data)
    ##    file = open('day4.txt', encoding='utf-8')

    pairs: list[tuple[str, str]] = []
    for line in file:
        section_pair = tuple(line.strip().split(",", 1))
        pairs.append(cast(tuple[str, str], section_pair))
    file.close()
    print(f"{part_one(pairs) = }")
    print(f"{part_two(pairs) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
