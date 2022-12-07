#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022 Day 3

"Advent of Code 2022 Day 3"

# Programmed by CoolCat467

__title__ = 'Advent of Code 2022 Day 3'
__author__ = 'CoolCat467'
__version__ = '0.0.0'

import io

Backpack = tuple[str, str]

def prioritize(item_type: str) -> int:
    "Get priority of item type"
    code = ord(item_type)
    if code > 90:
        return code - 96  # - 97 + 1
    return code - 38  # - 65 + 26 + 1

def part_one(backpacks: list[Backpack]) -> int:
    "Get sum of the priorities of items in both slots of each backpack"
    total = 0
    for slot_one, slot_two in backpacks:
        in_both = set(slot_one) & set(slot_two)
        total += sum(prioritize(item) for item in in_both)
    return total

def part_two(backpacks: list[Backpack]) -> int:
    "Get the sum of the priorities of the group sticker for each group"
    total = 0
    cur_group: list[str] = []
    for slot_one, slot_two in backpacks:
        cur_group.append(slot_one + slot_two)
        if len(cur_group) == 3:
            in_all = set(cur_group[-1])
            for item in cur_group:
                in_all &= set(item)
            total += sum(prioritize(item) for item in in_all)
            cur_group = []
    return total


def run() -> None:
    "Synchronous entry point"
    test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    file = io.StringIO(test_data)
##    file = open('day3.txt', encoding='utf-8')

    backpacks: list[Backpack] = []

    for line in file:
        contents = line.strip()
        count = len(contents)//2
        slot_one, slot_two = contents[:count], contents[count:]
        backpacks.append((slot_one, slot_two))
    file.close()
    print(f'{part_one(backpacks) = }')
    print(f'{part_two(backpacks) = }')

if __name__ == '__main__':
    print(f'{__title__}\nProgrammed by {__author__}.\n')
    run()
