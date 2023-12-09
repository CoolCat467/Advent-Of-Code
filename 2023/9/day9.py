"""Advent of Code 2023 Day 9."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 9"
__author__ = "CoolCat467"
__version__ = "0.0.0"

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


def read(text: str) -> tuple[tuple[int, ...], ...]:
    """Read numbers from text."""
    series: list[tuple[int, ...]] = []
    for line in text.splitlines():
        numbers = tuple(map(int, line.split(" ")))
        series.append(numbers)
    return tuple(series)


def delta(sequence: Iterable[int]) -> Generator[int, None, None]:
    """Yield deltas between each item in given sequence."""
    gen = iter(sequence)
    prev = next(gen)
    for next_ in gen:
        yield next_ - prev
        prev = next_


def extrapolate(sequence: tuple[int, ...]) -> int:
    """Extrapolate the next value of a given sequence."""
    deltas = tuple(delta(sequence))
    ##    print(deltas)
    different = set(deltas)
    if len(different) == 1:
        difference = next(iter(different))
        return difference + sequence[-1]
    return extrapolate(deltas) + sequence[-1]


def extrapolate_gen(sequence: tuple[int, ...]) -> Generator[int, None, None]:
    """Yield extrapolated values for new items of given sequence."""
    deltas = tuple(delta(sequence))
    ##    print(deltas)
    different = set(deltas)
    if len(different) == 1:
        difference = next(iter(different))
        count = 1
        while True:
            yield difference * count + sequence[-1]
            count += 1
    while True:
        for index, extrapolated_delta in enumerate(extrapolate_gen(deltas)):
            yield (index + 1) * extrapolated_delta + sequence[-1]


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    base = read(text)

    extrapolated_sum_forward = 0
    for sequence in base:
        value = next(extrapolate_gen(sequence))
        extrapolated_sum_forward += value

    extrapolated_sum_backward = 0
    for sequence in base:
        value = next(extrapolate_gen(tuple(reversed(sequence))))
        extrapolated_sum_backward += value

    return extrapolated_sum_forward, extrapolated_sum_backward


def run() -> None:
    """Print answer."""
    input_ = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    ##with open("day9.txt", encoding="utf-8") as file:
    ##    input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
