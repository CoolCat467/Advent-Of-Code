"""Advent of Code 2024 Day 7."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 7
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

__title__ = "Advent of Code 2024 Day 7"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


import operator
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import cast

##def find_ops(result: int, inputs: Sequence[str]) -> tuple[Sequence[tuple[str, ...]], bool]:
##    left, *rights = inputs
##    if not rights:
##        return (((),), result == int(left))
##    right = int(rights[0])
##    matches = []
##    for op in (operator.add, operator.mul):
##        ops_set, match = find_ops(result, (op(int(left), right), *rights[1:]))
##        if match:
##            for ops in ops_set:
##                matches.append((op.__name__, *ops))
##    return (matches, bool(matches))


def find_ops(result: int, inputs: Sequence[str]) -> bool:
    """Return if found successful string of operations to yield result."""
    # Get left most and maybe rights
    left, *rights = inputs
    int_left = int(left)
    # If left-most is too big, can't get any smaller so bad.
    if int_left > result:
        return False
    # If no more right items, return if left matches result
    if not rights:
        return int_left == result
    # If has right items, get right item
    right = int(rights[0])
    for op in (operator.add, operator.mul):
        # Perform operation
        # Recursive, pass to self with op result and all other right values
        # If returns true, match was successful
        if find_ops(result, (op(int_left, right), *rights[1:])):
            return True
    return False


##def find_ops_concat(result: int, inputs: Sequence[str]) -> tuple[Sequence[tuple[str, ...]], bool]:
##    left, *rights = inputs
##    if not rights:
##        return (((),), result == int(left))
##    right = rights[0]
##    matches = []
##    for op in (operator.add, operator.mul, operator.concat):
##        if op != operator.concat:
##            op_result = str(op(int(left), int(right)))
##        else:
##            op_result = op(left, right)
##        ops_set, match = find_ops_concat(result, (op_result, *rights[1:]))
##        if match:
##            for ops in ops_set:
##                matches.append((op.__name__, *ops))
##    return (matches, bool(matches))


def find_ops_concat(result: int, inputs: Sequence[str]) -> bool:
    """Return if found successful string of operations to yield result."""
    # Get left most and maybe rights
    left, *rights = inputs
    int_left = int(left)
    # If left-most is too big, can't get any smaller so bad.
    if int_left > result:
        return False
    # If no more right items, return if left matches result
    if not rights:
        return int_left == result
    # If has right items, get right item
    right = rights[0]
    int_right = int(right)
    for op in (operator.add, operator.mul, operator.concat):
        # Perform operation
        op_result: str
        if op == operator.concat:
            # Otherwise is concat and uses strings
            op_result = cast(Callable[[str, str], str], op)(left, right)
        else:
            # Needs int values
            fake_op = cast(Callable[[int, int], int], op)
            op_result = str(fake_op(int_left, int_right))
        # Recursive, pass to self with op result and all other right values
        # If returns true, match was successful
        if find_ops_concat(result, (op_result, *rights[1:])):
            return True
    return False


def run() -> None:
    """Run program."""
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    data_file = Path(__file__).absolute().parent / "day7.txt"
    if data_file.exists():
        data = data_file.read_text()

    part_one = 0
    part_two = 0
    for line in data.splitlines():
        # Get result and inputs
        result, input_ = line.split(": ", 1)
        result_int = int(result)
        input_values = input_.split(" ")
        # Check with part one
        if find_ops(result_int, input_values):
            # If success, add to both and can avoid processing with
            # part two which takes longer
            part_one += result_int
            part_two += result_int
        elif find_ops_concat(result_int, input_values):
            part_two += result_int
    print(f"{part_one = }")
    print(f"{part_two = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
