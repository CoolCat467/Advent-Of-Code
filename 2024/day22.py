"""Advent of Code 2224 Day 22."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2224 Day 22
# Copyright (C) 2224  CoolCat467
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

__title__ = "Advent of Code 2024 Day 22"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


def find_next_secret(current_secret: int) -> int:
    """Return next secret given current secret."""
    current_secret = (current_secret ^ (current_secret << 6)) % 0x1000000
    current_secret = (current_secret ^ (current_secret >> 5)) % 0x1000000
    return (current_secret ^ (current_secret << 11)) % 0x1000000


def find_secret_after_iterations(current_secret: int, count: int) -> int:
    """Return current secret after count iterations."""
    for _ in range(count):
        current_secret = find_next_secret(current_secret)
    return current_secret


def yield_next_secret(current_secret: int) -> Generator[int, None, None]:
    """Yield 2000 secret values given initial secret."""
    for _ in range(2000):
        yield current_secret
        current_secret = find_next_secret(current_secret)


def yield_next_price(initial_secret: int) -> Generator[int, None, None]:
    """Yield 2000 prices given initial secret value."""
    current_secret = initial_secret
    for _ in range(2000):
        current_secret = find_next_secret(current_secret)
        yield current_secret % 10


# Stolen from 2023 Day 9 and 2024 Day 2
def delta(sequence: Iterable[int]) -> Generator[tuple[int, int], None, None]:
    """Yield deltas between each item in given sequence."""
    gen = iter(sequence)
    prev = next(gen)
    for next_ in gen:
        yield next_ - prev, next_
        prev = next_


def calculate_delta_buffers(
    initial_secret: int,
) -> dict[tuple[int, int, int, int], int]:
    """Return mapping of deltas to price at that time."""
    delta_map: dict[tuple[int, int, int, int], int] = {}

    gen = delta(yield_next_price(initial_secret))
    first_three = (next(gen)[0], next(gen)[0], next(gen)[0])

    last_delta, price = next(gen)
    current = (*first_three, last_delta)

    delta_map[current] = price

    for last_delta, price in gen:
        current = (*current[1:], last_delta)
        if current in delta_map:
            continue
        delta_map[current] = price
    return delta_map


def run() -> None:
    """Run program."""
    data = """1
10
100
2024"""
    data = """1
2
3
2024"""
    data_file = Path(__file__).absolute().parent / "day22.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    secrets = tuple(map(int, data.splitlines()))

    sum_ = 0
    for secret in secrets:
        post = find_secret_after_iterations(secret, 2000)
        ##print((secret, post))
        sum_ += post
    print(f"{sum_ = }")

    ##gen = yield_next_secret(123)
    ##last = next(gen) % 10
    ##for _ in range(10):
    ##    secret_number = next(gen)
    ##    price = secret_number % 10
    ##    delta = price - last
    ##    last = price
    ##    print(f'{secret_number:>8}: {price} ({delta})')

    delta_price_map: Counter[tuple[int, int, int, int]] = Counter()
    for initial_secret in secrets:
        deltas = calculate_delta_buffers(initial_secret)
        delta_price_map.update(deltas)
    print(f"{delta_price_map.most_common(1) = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
