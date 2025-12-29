"""Advent of Code 2025 Day 3."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 3
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

__title__ = "Advent of Code 2025 Day 3"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

from mypy_extensions import i64, u8

if TYPE_CHECKING:
    from collections.abc import Generator


def yield_bank_matrix(
    bank: tuple[i64, ...],
) -> Generator[tuple[i64, ...], None, None]:
    """Yield bank matrix tuples."""
    for one_index, one in enumerate(bank):
        sub_bank: tuple[i64, ...] = ()
        one_x10 = one * 10
        for two in bank[one_index + 1 :]:
            sub_bank += (one_x10 + two,)
        yield sub_bank


def yield_bank_matrix_values(
    bank: tuple[i64, ...],
) -> Generator[i64, None, None]:
    """Yield bank matrix values."""
    for one_index, one in enumerate(bank):
        one_x10 = one * 10
        for two in bank[one_index + 1 :]:
            yield one_x10 + two


def yield_bank_matrix_values_generic_recursive(
    bank: tuple[i64, ...],
    count: u8 = 2,
) -> Generator[i64, None, None]:
    """Yield bank matrix numbers from {count} items in-order."""
    if count == 1:
        yield from bank
    else:
        for one_index, one in enumerate(bank):
            value = one * (10 ** (count - 1))
            for x in yield_bank_matrix_values_generic_recursive(
                bank[one_index + 1 :],
                count - 1,
            ):
                yield value + x


def find_largest(bank: tuple[i64, ...], count: u8 = 2) -> i64:
    """Return largest number from choosing {count} digits in-order."""
    # In one value case, very easy.
    if count == 1:
        return max(bank)
    assert count >= 0, "Can't find negative count digits!"

    # Get (index, digit) pairs in order
    order = list(enumerate(bank))
    order.sort(key=lambda tuple_: tuple_[1], reverse=True)

    for index, digit in order:
        if len(bank) - index < count:
            # print("bad: "+''.join(map(str, bank[index:])))
            continue
        return int(f"{digit}{find_largest(bank[index + 1 :], count - 1)}")
    raise ValueError(f"Missing values for bank ({bank = } {count = })")


def run() -> None:
    """Run program."""
    # Load data
    data = """987654321111111
811111111111119
234234234234278
818181911112111"""
    data_file = Path(__file__).absolute().parent / "day3.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data
    lines = data.splitlines()
    battery_banks = [tuple(map(i64, line)) for line in lines]
    # print("\n".join(map(repr, battery_banks)))

    # Part 1
    best_sum: i64 = 0
    for bank in battery_banks:
        ##print(f'{bank = }')
        ##print("\n".join(map(repr, yield_bank_matrix(bank))))
        # best = max(yield_bank_matrix_values(bank))
        best = find_largest(bank)
        best_sum += best
    print(f"{best_sum = }")

    # Part 2
    best_sum = 0
    for bank in battery_banks:
        # best = max(yield_bank_matrix_values_generic_recursive(bank, 12))
        best = find_largest(bank, 12)
        best_sum += best
    print(f"{best_sum = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
