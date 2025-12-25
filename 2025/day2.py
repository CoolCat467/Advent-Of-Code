"""Advent of Code 2025 Day 2."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 2
# Copyright (C) 2025  CoolCat467
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__title__ = "Advent of Code 2025 Day 2"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def get_digits(number: int) -> int:
    """Return number of digits in a number."""
    # return math.ceil(math.log10(number))
    return len(str(number))


def extract_digit(number: int, digit: int) -> int:
    """Return given digit of a number."""
    zeros: int = 10**digit
    return (number // zeros) % 10


def extract_digits(number: int) -> Generator[int, None, None]:
    """Yield the digits of a number."""
    yield from map(int, str(number))


def is_id_invalid(id_: int) -> bool:
    """Return if ID is invalid (Part 1)."""
    digits = get_digits(id_)
    if digits & 1:
        # odd number of digits
        return False
    half_length = digits // 2
    all_digits = tuple(extract_digits(id_))
    first_half = all_digits[:half_length]
    second_half = all_digits[half_length:]
    # if first_half == second_half:
    #     print(f'\n{id_ = }\n{digits = }\n{half_length = }\n{first_half  = }\n{second_half = }')
    return first_half == second_half


def is_id_invalid_two(id_: int) -> bool:
    """Return if ID is invalid (Part 2)."""
    all_digits = tuple(extract_digits(id_))
    digits = len(all_digits)
    for divisor in range(2, digits + 1):
        size = digits // divisor
        if size * divisor < digits:
            continue
        if size == digits:
            continue
        # print(f'{size = }')
        slice_indexes = (*range(0, digits, size), digits)
        prior: tuple[int, ...] | None = None
        for index in range(len(slice_indexes) - 1):
            start = slice_indexes[index]
            stop = slice_indexes[index + 1]
            fragment = all_digits[start:stop]
            if prior is not None and fragment != prior:
                break
            prior = fragment
        else:
            return True
    return False


def run() -> None:
    """Run program."""
    # Load data
    data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""
    data_file = Path(__file__).absolute().parent / "day2.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    ranges = data.split(",")
    id_pairs = tuple(
        tuple(map(int, range_.split("-", 1))) for range_ in ranges
    )
    # print("\n".join(map(repr, id_pairs)))

    # Part 1
    invalid_sum = 0
    for range_ in id_pairs:
        for id_ in range(*range_):
            if is_id_invalid(id_):
                #             print(f'bad {id_ = }')
                invalid_sum += id_
    print(f"{invalid_sum = }")

    # Part 2
    invalid_sum = 0

    # print(f'{is_id_invalid_two(123120) = }')
    for range_ in id_pairs:
        for id_ in range(*range_):
            if is_id_invalid_two(id_):
                #             print(f'bad {id_ = }')
                invalid_sum += id_
    print(f"{invalid_sum = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
