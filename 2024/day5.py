"""Advent of Code 2024 Day 5."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 5
# Copyright (C) 2024  CoolCat467
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

__title__ = "Advent of Code 2024 Day 5"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def is_order_correct(
    order: Sequence[int],
    rules: set[tuple[int, int]],
) -> bool:
    """Return if print order is correct."""
    # Get left element
    left, *rest = order
    # If no more items, last element, so correct
    if not rest:
        return True
    # Otherwise, make sure rule for all following elements exist
    for right in rest:
        if (left, right) not in rules:
            # Rule not exist, bad
            return False
    # Recursive, leftmost is good, need to check next set.
    return is_order_correct(rest, rules)


def fix_update(
    order: Sequence[int],
    rules: set[tuple[int, int]],
) -> tuple[int, ...]:
    """Return fixed print order."""
    for index, left in enumerate(order):
        for index2, right in enumerate(order):
            # Ignore same element
            if index == index2:
                continue
            if (left, right) not in rules:
                # Entire set for left element is bad
                break
        else:
            # If continued without hitting break
            # Convert to list if it isn't already one
            if not isinstance(order, list):
                order = list(order)
            # Remove found correct left element
            order.remove(left)
            # Recursive, find rest of correct elements
            return (left, *fix_update(order, rules))
    if order:
        raise ValueError("No possible solution with given rule set!")
    # If fell through to here, no items to re-order.
    # Adding to blank tuple is same tuple
    return ()


def run() -> None:
    """Run program."""
    data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    data = Path("day5.txt").read_text()
    rules: set[tuple[int, int]] = set()
    gen = iter(data.splitlines())
    for line in gen:
        # Read rules until blank line
        if not line:
            break
        before, after = map(int, line.split("|"))
        rules.add((before, after))
    updates: list[tuple[int, ...]] = []
    # Remaining items are updates to perform
    for line in gen:
        updates.append(tuple(map(int, line.split(","))))

    part_one = 0
    part_two = 0
    for update in updates:
        if is_order_correct(update, rules):
            part_one += update[len(update) // 2]
        else:
            corrected_update = fix_update(update, rules)
            assert is_order_correct(corrected_update, rules)
            part_two += corrected_update[len(update) // 2]
    print(f"{part_one = }")
    print(f"{part_two = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
