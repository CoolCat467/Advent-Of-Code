#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 5

"Advent of Code 2022 Day 5."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 5"
__author__ = "CoolCat467"
__version__ = "0.0.0"


import io
import json
from collections import deque


def deep_copy_deque(stack: dict[int, deque[str]]) -> dict[int, deque[str]]:
    "Deep copy stack."  # noqa: D300

    def encode_deque(obj: object) -> object:
        if isinstance(obj, deque):
            return list(obj)
        raise TypeError(
            f"Object of type {obj.__class__.__name__} "
            f"is not JSON serializable",
        )

    dict_ = json.loads(json.dumps(stack, default=encode_deque))
    return {int(k): deque(v) for k, v in dict_.items()}


def part_one(
    stack: dict[int, deque[str]],
    instructions: list[tuple[int, int, int]],
) -> str:
    "Get topmost crates from following instructions moving one box at a time."  # noqa: D300
    for count, from_, to in instructions:
        for _ in range(count):
            stack[to].appendleft(stack[from_].popleft())
    topmost = []
    for idx in sorted(stack):
        topmost.append(stack[idx][0])
    return "".join(topmost)


def part_two(
    stack: dict[int, deque[str]],
    instructions: list[tuple[int, int, int]],
) -> str:
    "Crane is actually pro and can move more than one box at once."  # noqa: D300
    for count, from_, to in instructions:
        values = []
        for _ in range(count):
            values.append(stack[from_].popleft())
        stack[to].extendleft(reversed(values))
    topmost = []
    for idx in sorted(stack):
        topmost.append(stack[idx][0])
    return "".join(topmost)


def group_every(line: str, every: int, sep: int) -> list[str]:
    "Return groups from every {every} characters of line with separator."  # noqa: D300
    groups = []
    total_char = len(line)
    group_count = 0
    while group_count * every + max(group_count - 1, 0) * sep < total_char:
        group_count += 1
    group_count -= 1

    for section in range(group_count):
        start = section * every + section * sep
        groups.append(line[start : start + every])
    return groups


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    file = io.StringIO(test_data)
    ##    file = open('day5.txt', encoding='utf-8')

    stack: dict[int, deque[str]] = {}
    instructions: list[tuple[int, int, int]] = []
    is_stack = True
    for line in file:
        if not is_stack:
            data = line.strip().split(" ")
            save = tuple(map(int, (data[1], data[3], data[5])))
            instructions.append((save[0], save[1] - 1, save[2] - 1))
            continue
        if not line.strip():
            is_stack = False
            continue
        groups = [x.strip() for x in group_every(line, 3, 1)]
        for stack_idx, create in enumerate(groups):
            if stack_idx not in stack:
                stack[stack_idx] = deque()
            if not create:
                continue
            if create.isdigit():
                break
            stack[stack_idx].append(create[1:-1])
    file.close()
    ##    print(f'{stack = }')
    ##    print(f'{instructions = }')
    stack_copy = deep_copy_deque(stack)
    print(f"{part_one(stack_copy, instructions) = }")
    print(f"{part_two(stack, instructions) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
