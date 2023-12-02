"""2023 Day 1."""

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "2023 Day 1"
__author__ = "CoolCat467"


import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

DIGIT_REGEX = re.compile(r"\d")
DIGITS = (
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)
TEXT_DIGITS = re.compile(f"\\d|{'|'.join(DIGITS)}")


def parse_digits_one(line: str) -> Generator[int, None, None]:
    """Return generator of numerical digits from line."""
    return (int(x.group(0)) for x in DIGIT_REGEX.finditer(line))


def parse_digits_two(line: str) -> Generator[int, None, None]:
    """Return generator of numerical and alphanumerical digits from line."""
    # Hack to fix it:
    line = (
        line.replace("eightwo", "82")
        .replace("twone", "21")
        .replace("oneight", "18")
    )
    for match in TEXT_DIGITS.finditer(line):
        value = match.group(0)
        try:
            yield int(value)
        except ValueError:
            yield DIGITS.index(value) + 1


def process(text: str) -> tuple[int, int]:
    """Return answers to problems one and two given input text."""
    values_one = []
    values_two = []
    for line in text.splitlines():
        numbers_one = tuple(parse_digits_one(line))
        values_one.append(int(f"{numbers_one[0]}{numbers_one[-1]}"))

        numbers_two = tuple(parse_digits_two(line))
        values_two.append(int(f"{numbers_two[0]}{numbers_two[-1]}"))
    return sum(values_one), sum(values_two)


def run() -> None:
    """Run program."""
    ##    input_ = """1abc2
    ##pqr3stu8vwx
    ##a1b2c3d4e5f
    ##treb7uchet"""
    input_ = """two1nine
eightwo2three
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    ##    with open("day1.txt", encoding="utf-8") as file:
    ##        input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
