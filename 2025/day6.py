"""Advent of Code 2025 Day 6."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2025 Day 6
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

__title__ = "Advent of Code 2025 Day 6"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path


def run() -> None:
    """Run program."""
    # Load data
    data = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """
    data_file = Path(__file__).absolute().parent / "day6.txt"
    if data_file.exists():
        data = data_file.read_text()

    # Parse data part 1
    rows: list[tuple[int, ...]] = []
    *lines, raw_ops = data.splitlines()
    ops = tuple(raw_ops.split())
    for line in lines:
        rows.append(tuple(map(int, line.split())))
    # print('\n'.join(map(repr, rows)))
    # print(ops)

    # Part 1
    grand_total = 0
    for index, op in enumerate(ops):
        value = 0
        if op == "*":
            value = 1
        for row in rows:
            if op == "+":
                value += row[index]
            elif op == "*":
                value *= row[index]
            else:
                raise NotImplementedError(f"{op = }")
        grand_total += value
    print(f"{grand_total = }")

    # Parse data part 2
    start_columns: list[int] = []
    # print(f'{raw_ops = }')
    for index, char in enumerate(raw_ops):
        if char != " ":
            start_columns.append(index)
    start_columns.append(len(lines[0]) + 1)

    # print(f'{start_columns = }')
    rows.clear()
    for start_index, start in enumerate(start_columns[:-1]):
        end = start_columns[start_index + 1] - 2
        # print(f'{start, end = }')
        for column in range(start, end + 1):
            value_str = ""
            for line in lines:
                value_str += line[column]
            # print(f'{value_str = }', end=' ')
            value = int(value_str.strip())
            # print(f'{value = }')
            row += (value,)
        rows.append(row)

    # print('\n'.join(map(repr, rows)))
    # print(ops)

    # Part 2
    grand_total = 0
    for index, op in enumerate(ops):
        value = 0
        if op == "*":
            value = 1
        for column in rows[index]:
            if op == "+":
                value += column
            elif op == "*":
                value *= column
            else:
                raise NotImplementedError(f"{op = }")
        # print(f'{value = }')
        grand_total += value
    print(f"{grand_total = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
