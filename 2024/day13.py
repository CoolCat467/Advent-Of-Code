"""Advent of Code 2024 Day 13."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 13
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

__title__ = "Advent of Code 2024 Day 13"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import NamedTuple

import numpy as np
from vector import Vector2


def vec2_to_int(vec: Vector2) -> tuple[int, int]:
    """Help mypy understand Vector2 is same as tuple[int, int]."""
    x, y = vec
    return int(x), int(y)


class Machine(NamedTuple):
    """Claw machine data."""

    button_a: Vector2
    button_b: Vector2
    prize: Vector2


def read_vec2(delta: str) -> Vector2:
    """Return Vector2 from delta/total string."""
    body = delta.split(": ", 1)[1]
    x_str, y_str = body.split(", ", 1)
    return Vector2(
        int(x_str.removeprefix("X").removeprefix("=")),
        int(y_str.removeprefix("Y").removeprefix("=")),
    )


def read_machine(machine_group: str) -> Machine:
    """Return Machine object from machine data group."""
    gen = iter(machine_group.splitlines())
    button_a = read_vec2(next(gen))
    button_b = read_vec2(next(gen))
    prize = read_vec2(next(gen))
    return Machine(button_a, button_b, prize)


def read_machines(data: str) -> tuple[Machine, ...]:
    """Return tuple of Machine objects from data."""
    machines = []
    for machine_group in data.split("\n\n"):
        machines.append(read_machine(machine_group))
    return tuple(machines)


def find_press_counts(
    machine: Machine,
    initial_pos: Vector2 | None = None,
) -> Vector2 | None:
    """Return press counts for each button or None if no integer answer."""
    if initial_pos is None:
        initial_pos = Vector2(0, 0)
    difference = machine.prize + initial_pos

    ##print(f'{machine.button_a.x} * x1 + {machine.button_b.x} * x2 = {difference.x}')
    ##print(f'{machine.button_a.y} * x1 + {machine.button_b.y} * x2 = {difference.y}')

    ##matrix = Matrix(
    ##    [machine.button_a.x, machine.button_b.x,
    ##     machine.button_a.y, machine.button_b.y],
    ##    (2, 2),
    ##)
    ##inverse = matrix.inverse()
    ##solved = Vector2.from_iter(inverse @ difference).floored()
    matrix = np.array(
        (
            machine.button_a,
            machine.button_b,
        ),
        dtype=np.uint64,
    ).T
    # Transpose so x and y are in own rows instead of columns
    inverse = np.linalg.inv(matrix)

    # Get solution
    # Answer might not be whole numbers however, meaning invalid answer.
    solved = Vector2.from_iter(inverse @ vec2_to_int(difference)).floored()

    # With flooring, we can be a hair off from reality
    for dx in range(2):
        for dy in range(2):
            # Ruff thinks these are tuples and we want to concat
            # They are indeed tuples, but want to do actual component-wise
            # add instead of tuple concat.
            solution = solved + (dx, dy)  # noqa: RUF005
            result = (
                solution[0] * machine.button_a + solution[1] * machine.button_b
            )
            if result == difference:
                ##print(f'{(dx, dy)}')
                return solution

    return None


def run() -> None:
    """Run program."""
    data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    data_file = Path(__file__).absolute().parent / "day13.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    # Parse machines data
    machines = read_machines(data)

    total_tokens = 0
    total_tokens_two = 0
    initial_two = Vector2(10000000000000, 10000000000000)
    for machine in machines:
        press_counts = find_press_counts(machine)
        if press_counts is not None:
            total_tokens += int(press_counts @ (3, 1))

        press_counts = find_press_counts(machine, initial_two)
        if press_counts is not None:
            total_tokens_two += int(press_counts @ (3, 1))
    print(f"{total_tokens = }")
    print(f"{total_tokens_two = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
