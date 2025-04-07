#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 13

"Advent of Code 2022 Day 13."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 13"
__author__ = "CoolCat467"
__version__ = "0.0.0"


import functools
import io
import json
import operator
from typing import Any, cast

Packet = int | list[int] | list[list[Any]]


def get_value(string: str) -> Packet:
    "Get object from string."  # noqa: D300
    return cast("Packet", json.loads(string))


def compare(left: Packet, right: Packet) -> bool | None:
    "Return true if in right order."  # noqa: D300
    ##    print(f'{left} {right}')
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, int) or isinstance(right, int):
        if isinstance(left, int):
            return compare([left], right)
        if isinstance(right, int):
            return compare(left, [right])
    else:
        for left_val, right_val in zip(left, right, strict=False):
            state = compare(cast("Packet", left_val), cast("Packet", right_val))
            if state is None:
                continue
            return state
        if len(left) == len(right):
            return None
        return len(left) < len(right)
    return None


def part_one(pairs: list[tuple[str, str]]) -> int:
    "Calculate sum of indexes of correct pairs."  # noqa: D300
    correct_index_sum = 0
    current = 1
    for str_left, str_right in pairs:
        left = get_value(str_left)
        right = get_value(str_right)
        state = compare(left, right)
        ##        print(f'{current}: {state}')
        if state:
            correct_index_sum += current
        current += 1
    return correct_index_sum


def part_two(pairs: list[tuple[str, str]]) -> int:
    "Calculate the decoder key for the distress signal."  # noqa: D300
    values: list[str] = functools.reduce(
        operator.iadd,
        (list(pair) for pair in pairs),
        [],
    )
    dividers = ("[[2]]", "[[6]]")
    values.extend(dividers)
    ordered: list[str] = [values[0]]
    for value in values[1:]:
        ordered.append(value)
        length = len(ordered)
        i = length - 2
        while i >= 0 and compare(
            get_value(ordered[i + 1]),
            get_value(ordered[i]),
        ):
            left, right = ordered[i], ordered[i + 1]
            ordered[i + 1], ordered[i] = left, right
            i -= 1
    ##    print('\n'.join(ordered))
    return (1 + ordered.index(dividers[0])) * (1 + ordered.index(dividers[1]))


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    file = io.StringIO(test_data)
    ##    file = open('day13.txt', encoding='utf-8')

    pairs: list[tuple[str, str]] = []

    for line in file:
        if line == "\n":
            continue
        pairs.append((line.strip(), file.readline().strip()))

    file.close()

    print(f"{part_one(pairs) = }")
    print(f"{part_two(pairs) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
