#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 10

"Advent of Code 2022 Day 10."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 10"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import io
from collections import deque
from dataclasses import dataclass
from typing import Final, Generator


@dataclass(slots=True)
class Instruction:
    "Instruction."  # noqa: D300
    name: str
    arguments: tuple[int, ...]


CYCLES: Final = {"noop": 1, "addx": 2}


def cpu_generator() -> (
    Generator[
        tuple[dict[str, int], tuple[Instruction | None, int], bool],
        list[Instruction] | Instruction | None,
        None,
    ]
):
    "CPU Generator."  # noqa: D300
    registers: dict[str, int] = {"X": 1}
    buffer: deque[Instruction] = deque()

    instruction: Instruction | None = None
    cycles_left = 0

    while True:
        new_data = yield (
            registers,
            (instruction, cycles_left),
            bool(buffer) or bool(cycles_left),
        )

        if new_data is None:
            new_instructions = []
        elif isinstance(new_data, Instruction):
            new_instructions = [new_data]
        else:
            new_instructions = new_data

        buffer.extendleft(new_instructions)

        if cycles_left > 0:
            cycles_left -= 1
            continue
        if instruction is not None:
            if instruction.name == "noop":
                pass
            elif instruction.name.startswith("add"):
                register = instruction.name.removeprefix("add").upper()
                registers[register] += instruction.arguments[0]
            else:
                raise NotImplementedError(
                    f'Instruction "{instruction.name}" not implemented',
                )

        if not buffer:
            continue

        instruction = buffer.pop()
        cycles_left = CYCLES[instruction.name] - 1


def part_one(instructions: list[Instruction]) -> int:
    "Calculate the sum of the signal strengths."  # noqa: D300
    ##    cpu = cpu_generator()
    ##    cpu.send(None)
    ##    cpu.send(instructions)
    ##
    ##    processing = True
    ##
    ##    sum_signals = 0
    ##
    ##    cycle = 0
    ##    while processing:
    ##        registers, process, processing = next(cpu)
    ##        if processing:
    ##            cycle += 1
    ####        print((registers, process, processing))
    ##        if (cycle-20) % 40 == 0:
    ##            print((cycle, registers, process))
    ####            print(f'{cycle = } {registers["X"] = }')
    ##            sum_signals += cycle * registers['X']
    ####        else:
    ####            print((registers, process))
    ##    cpu.close()
    ##
    ##    return sum_signals
    sum_signals = 0

    cycle = 0
    registers = {"X": 1}

    def wait(cycles: int) -> None:
        nonlocal cycle, sum_signals, registers
        for _ in range(cycles):
            cycle += 1
            if (cycle - 20) % 40 == 0:
                sum_signals += cycle * registers["X"]

    for instruction in instructions:
        if instruction.name == "noop":
            wait(1)
        elif instruction.name.startswith("add"):
            register = instruction.name.removeprefix("add").upper()
            wait(2)
            registers[register] += instruction.arguments[0]
        else:
            raise NotImplementedError(
                f'Instruction "{instruction.name}" not implemented',
            )
    return sum_signals


def part_two(instructions: list[Instruction]) -> str:
    "Render sprite and get text answer."  # noqa: D300
    viewport = ""
    cycle = 0
    registers = {"X": 1}

    def wait(cycles: int) -> None:
        nonlocal cycle, registers, viewport
        for _ in range(cycles):
            cycle += 1
            crt_pos = cycle % 40
            x = registers["X"]
            if crt_pos in range(x, x + 3):
                viewport += "#"
            else:
                viewport += " "
            if crt_pos == 0:
                viewport += "\n"

    for instruction in instructions:
        if instruction.name == "noop":
            wait(1)
        elif instruction.name.startswith("add"):
            register = instruction.name.removeprefix("add").upper()
            wait(2)
            registers[register] += instruction.arguments[0]
        else:
            raise NotImplementedError(
                f'Instruction "{instruction.name}" not implemented',
            )
    return viewport


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

    instructions: list[Instruction] = []

    file = io.StringIO(test_data)
    ##    file = open('day10.txt', encoding='utf-8')

    for line in file:
        command, *arguments = line.strip().split(" ")
        instructions.append(Instruction(command, tuple(map(int, arguments))))

    file.close()

    print(f"{part_one(instructions) = }")
    print(f"part_two(instructions) = \n{part_two(instructions)}")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
