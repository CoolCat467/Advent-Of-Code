"""Advent of Code 2023 Day 6."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 6"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import math
import re
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Generator

NUMBER_REGEX: Final = re.compile(r"\d+")


def find_numbers(line: str) -> Generator[int, None, None]:
    """Yield number matches in given line."""
    for match in NUMBER_REGEX.finditer(line):
        yield int(match.group(0))


def part_one(text: str) -> int:
    """Return error margin from part one."""
    time_str, distance_str = (line.split(":")[1] for line in text.splitlines())
    races = tuple(zip(find_numbers(time_str), find_numbers(distance_str)))
    error_margin = 1
    for time, record_distance in races:
        ways_to_win = 0
        for sec in range(time + 1):
            speed = sec
            travel_time = time - sec
            distance = speed * travel_time
            if distance > record_distance:
                ways_to_win += 1
        error_margin *= ways_to_win
    return error_margin


def get_distance(cur_time: int, max_time: int) -> int:
    """Return distance traveled if you wait cur_time milliseconds out of max_time."""
    return cur_time * (max_time - cur_time)


def does_win(cur_time: int, max_time: int, record_distance: int) -> bool:
    """Return if you win given time, max time, and record distance."""
    return get_distance(cur_time, max_time) > record_distance


def find_left(
    min_time: int,
    max_time: int,
    time: int,
    record_distance: int,
) -> int:
    """Find left bound win change."""
    ##    print(f'{min_time} {max_time}')
    if min_time == max_time or min_time + 1 == max_time:
        return min_time
    half = math.ceil((min_time + max_time) / 2)
    if does_win(half, time, record_distance):
        return find_left(min_time, half, time, record_distance)
    return find_left(half, max_time, time, record_distance)


def find_right(
    min_time: int,
    max_time: int,
    time: int,
    record_distance: int,
) -> int:
    """Find right bound win change."""
    ##    print(f'{min_time} {max_time}')
    if min_time == max_time or min_time + 1 == max_time:
        return min_time
    half = math.ceil((min_time + max_time) / 2)
    if does_win(half, time, record_distance):
        return find_right(half, max_time, time, record_distance)
    return find_right(0, half, time, record_distance)


def part_two(time: int, record_distance: int) -> int:
    """Return number of ways we can win in part two."""
    left_bound = find_left(0, time, time, record_distance) + 1
    left = left_bound
    ##    print(f'{left_bound = }')
    for x in range(-2, 2):
        left = left_bound + x
        win = does_win(left, time, record_distance)
        ##        print(f'{left} {win}')
        if win:
            break
    right_bound = find_right(left_bound, time, time, record_distance) + 1
    ##    print(f'{right_bound = }')
    right = right_bound
    for x in range(-2, 2):
        right = right_bound + x
        win = does_win(right, time, record_distance)
        ##        print(f'{right} {win}')
        if not win:
            break
    return right - left


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    error_margin = part_one(text)
    data = (line.split(":")[1].replace(" ", "") for line in text.splitlines())
    time, record_distance = find_numbers(" ".join(data))
    ways_to_win = part_two(time, record_distance)

    return error_margin, ways_to_win


def run() -> None:
    """Print answer."""
    input_ = """Time:      7  15   30
Distance:  9  40  200"""
    ##with open("day6.txt", encoding="utf-8") as file:
    ##    input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
