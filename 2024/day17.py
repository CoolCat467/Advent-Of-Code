"""Advent of Code 2024 Day 17."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 17
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

__title__ = "Advent of Code 2024 Day 17"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Generator
import dataclasses

from mypy_extensions import u8

INST_LOOKUP: Final = ("adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv")


@dataclasses.dataclass(slots=True)
class Computer:
    """Computer dataclass."""

    reg_a: int = 0
    reg_b: int = 0
    reg_c: int = 0
    ip: u8 = 0
    output: list[u8] = dataclasses.field(default_factory=list)

    def combo_op(self, operand: int) -> int:
        """Return combo-operator value."""
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.reg_a,
            5: self.reg_b,
            6: self.reg_c,
        }[operand]

    def incr_ip(self) -> None:
        """Increment instruction pointer."""
        self.ip += 2

    def inst_adv(self, operand: int) -> None:
        """Add floor divide register A by 2 ** combo op."""
        self.reg_a //= 1 << self.combo_op(operand)
        self.incr_ip()

    def inst_bxl(self, operand: int) -> None:
        """Xor register B by operand."""
        self.reg_b ^= operand
        self.incr_ip()

    def inst_bst(self, operand: int) -> None:
        """Set register b to combo op modulo 8."""
        self.reg_b = self.combo_op(operand) % 8
        self.incr_ip()

    def inst_jnz(self, operand: int) -> None:
        """Jump to operand literal value if A is nonzero."""
        if self.reg_a == 0:
            self.incr_ip()
            return
        self.ip = operand

    def inst_bxc(self, _operand: int) -> None:
        """Xor register B by register C."""
        self.reg_b ^= self.reg_c
        self.incr_ip()

    def inst_out(self, operand: int) -> None:
        """Add combo operand modulo 8 to output."""
        self.output.append(self.combo_op(operand) % 8)
        self.incr_ip()

    def inst_bdv(self, operand: int) -> None:
        """Set register B to result of A floor divide by 2 ** combo operand."""
        self.reg_b = self.reg_a // (1 << self.combo_op(operand))
        self.incr_ip()

    def inst_cdv(self, operand: int) -> None:
        """Set register C to result of A floor divide by 2 ** combo operand."""
        self.reg_c = self.reg_a // (1 << self.combo_op(operand))
        self.incr_ip()

    def op_to_inst(self, opcode: int) -> str:
        """Get instruction string from opcode."""
        return INST_LOOKUP[opcode]

    def reset(self, reg_a: int, reg_b: int, reg_c: int) -> None:
        """Reset computer state."""
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.output.clear()

    def run_program(self, data: tuple[u8, ...]) -> None:
        """Run program."""
        self.ip = u8(0)
        while int(self.ip) < len(data):
            opcode = data[self.ip]
            operand = data[self.ip + 1]

            name = self.op_to_inst(opcode)
            function = getattr(self, f"inst_{name}")
            function(operand)

    def program_gen(self, data: tuple[u8, ...]) -> Generator[int, None, None]:
        """Yield program output values."""
        self.ip = 0

        while int(self.ip) < len(data):
            opcode = data[self.ip]
            operand = data[self.ip + 1]

            name = self.op_to_inst(opcode)
            function = getattr(self, f"inst_{name}")
            function(operand)

            if name == "out":
                yield self.output[-1]

    def run_program_expecting(self, data: tuple[u8, ...]) -> bool:
        """Return if program output matches input."""
        # Tried to optimize to run better with mypyc
        self.ip = 0
        index = 0
        while int(self.ip) < len(data):
            opcode = data[self.ip]
            operand = data[self.ip + 1]

            if opcode == 0:
                self.inst_adv(operand)
            elif opcode == 1:
                self.inst_bxl(operand)
            elif opcode == 2:
                self.inst_bst(operand)
            elif opcode == 3:
                self.inst_jnz(operand)
            elif opcode == 4:
                self.inst_bxc(operand)
            elif opcode == 5:
                self.inst_out(operand)
                if data[index] != self.output[index]:
                    break
                index += 1
                if index >= len(data):
                    self.output.append(9999)
                    break
            elif opcode == 6:
                self.inst_bdv(operand)
            elif opcode == 7:
                self.inst_cdv(operand)
        return tuple(self.output) == data


def combo_op_str(operand: int) -> str:
    """Return combo-operator value."""
    return {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "A",
        5: "B",
        6: "C",
    }[operand]


def print_program(data: tuple[u8, ...]) -> None:
    """Print out program readout from input."""
    for idx in range(0, len(data), 2):
        opcode = data[idx]
        operand = data[idx + 1]

        if opcode == 0:  # adv
            print(f"A //= (1 << {combo_op_str(operand)})")
        if opcode == 1:  # bxl
            print(f"B ^= {operand}")
        if opcode == 2:  # bst
            print(f"B = {combo_op_str(operand)} & 0b111")
        if opcode == 3:  # jnz
            print(f"if A != 0: goto {operand}")
        if opcode == 4:  # bxc
            print("B ^= C")
        if opcode == 5:  # out
            print(f"print({combo_op_str(operand)} & 0b111)")
        if opcode == 6:  # bdv
            print(f"B = A // (1 << {combo_op_str(operand)})")
        if opcode == 7:  # cdv
            print(f"C = A // (1 << {combo_op_str(operand)})")


def program_real(a: int) -> tuple[int, ...]:
    """Return output of program given register A's value."""
    out = []
    while True:
        b = a & 0b111
        c = a // (1 << (b ^ 7)) & 0b111
        out.append(b ^ c)
        a >>= 3
        if a == 0:
            break
    return tuple(out)


def reconstruct_a(out: tuple[int, ...]) -> int:
    """Rebuild register A's initial value given desired output."""
    # Created with help from ChatGPT 4o mini

    # Start with a = 0 as a potential value
    potential_a_values = {0}

    for value in reversed(out):
        new_potential_a_values = set()
        # We need to find B and C such that B ^ C = value
        # B can be 0 to 7 (0b000 to 0b111)
        for b in range(8):
            c = b ^ value
            for a in potential_a_values:
                # Calculate the potential a value
                # Shift a left by 3 bits and add b
                potential_a = (a << 3) | b
                # Check if c can be derived from potential_a
                if (potential_a // (1 << (b ^ 7)) & 0b111) == c:
                    new_potential_a_values.add(potential_a)
        # Update potential values for the next iteration
        potential_a_values = new_potential_a_values

    # Return the smallest valid a found
    return min(potential_a_values) if potential_a_values else 0


def run() -> None:
    """Run program."""
    data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    data = """Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
    data_file = Path(__file__).absolute().parent / "day17.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    gen = iter(data.splitlines())
    reg_a = int(next(gen).split(": ")[1])
    reg_b = int(next(gen).split(": ")[1])
    reg_c = int(next(gen).split(": ")[1])
    next(gen)
    program = tuple(map(u8, next(gen).split(": ")[1].split(",")))

    computer = Computer(reg_a, reg_b, reg_c)
    print(f"{computer = }")
    computer.run_program(program)
    output = ",".join(map(str, computer.output))
    print(f"{output = }")

    print("\nprogram = " + ",".join(map(str, program)))
    print()

    print_program(program)
    print()

    # I tried brute forcing it and compiled with mypyc and got up
    # to 302_000_000, but that was taking too long.
    ##reg_a = 302000000
    ##computer = Computer(reg_a, reg_b, reg_c)
    ##while True:
    ##    if not reg_a % 1000000:
    ##        print(f"{reg_a = }")
    ##    computer.reset(reg_a, reg_b, reg_c)
    ##    if computer.run_program_expecting(program):
    ##        break
    ##    reg_a += 1
    ##print(f"{reg_a = }")

    reg_a = reconstruct_a((2, 4, 1, 7, 7, 5, 0, 3, 4, 4, 1, 7, 5, 5, 3, 0))
    print(f"{reg_a = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
