"""Advent of Code 2023 Day 8."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 8"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import math


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    instructions_line, node_lines = text.split("\n\n")

    instructions = tuple("LR".index(char) for char in instructions_line)

    nodes: dict[str, tuple[str, str]] = {}
    for line in node_lines.splitlines():
        name, ends = line.split(" = ")
        left, right = ends[1:-1].split(", ")
        nodes[name] = (left, right)

    steps_one = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        instruction = instructions[steps_one % len(instructions)]
        current_node = nodes[current_node][instruction]
        steps_one += 1

    ends_after = set()
    for start_node in (name for name in nodes if name.endswith("A")):
        current_node = start_node
        steps = 0
        while not current_node.endswith("Z"):
            instruction = instructions[steps % len(instructions)]
            current_node = nodes[current_node][instruction]
            steps += 1
        ends_after.add(steps)

    steps_two = math.lcm(*ends_after)

    return steps_one, steps_two


def run() -> None:
    """Print answer."""
    input_ = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    with open("day8.txt", encoding="utf-8") as file:
        input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
