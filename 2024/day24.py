"""Advent of Code 2024 Day 24."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 24
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

__title__ = "Advent of Code 2024 Day 24"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from enum import IntEnum, auto
from pathlib import Path
from typing import NamedTuple, Self


class Op(IntEnum):
    """Operator type."""

    AND = 0
    OR = auto()
    XOR = auto()


class Expr(NamedTuple):
    """Expression type."""

    one: str | Expr
    two: str | Expr
    op: Op

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Return Expr instance from string."""
        left, op, right = string.split(" ", 2)
        left, right = sorted((left, right))
        return cls(
            left,
            right,
            getattr(Op, op),
        )

    def calculate_value(self, wire_states: dict[str, int]) -> int | None:
        """Calculate value given wire states."""
        assert isinstance(self.one, str)
        assert isinstance(self.two, str)
        one_value = wire_states.get(self.one)
        if one_value is None:
            return None
        two_value = wire_states.get(self.two)
        if two_value is None:
            return None
        if self.op == Op.OR:
            return one_value | two_value
        if self.op == Op.AND:
            return one_value & two_value
        if self.op == Op.XOR:
            return one_value ^ two_value
        raise NotImplementedError(self.op)

    def as_code(self) -> str:
        """Return string representation of expression."""
        op = {
            Op.OR: "|",
            Op.AND: "&",
            Op.XOR: "^",
        }[self.op]
        if self.one == self.two:
            if self.op in (Op.OR, Op.AND):
                return f"{self.one}"
            return "0"
        one, two = sorted((self.one, self.two))
        return f"({one} {op} {two})"


def get_expr(num: int, op: str) -> str:
    """Return expression code for x and y of number with operator."""
    return f"(x{num:02} {op} y{num:02})"


def find_last_carry(num: int) -> str:
    """Return expression code for the carry value of last bit."""
    carry = get_expr(num - 1, "&")
    if num == 1:
        return carry
    last_add = get_expr(num - 1, "^")
    last_carry = find_last_carry(num - 1)
    return f"(({last_carry} & {last_add}) | {carry})"


def find_add(num: int, max_bits: int = 45) -> str:
    """Return expression code for adding given bit."""
    current = get_expr(num, "^")
    if num == 0:
        return current  # No carry for the least significant bit
    carry = find_last_carry(min(num, max_bits))
    if num >= max_bits:
        return carry
    return f"({carry} ^ {current})"


def get_expr_expr(num: int, op: str) -> Expr:
    """Return Expr object for op of x and y of given bit."""
    return Expr(f"x{num:02}", f"y{num:02}", {"^": Op.XOR, "&": Op.AND}[op])


def find_last_carry_expr(num: int) -> Expr:
    """Return carry Expr object for given bit."""
    carry = get_expr_expr(num - 1, "&")
    if num == 1:
        return carry
    last_add = get_expr_expr(num - 1, "^")
    last_carry = find_last_carry_expr(num - 1)
    return Expr(Expr(last_carry, last_add, Op.AND), carry, Op.OR)


def find_add_expr(num: int, max_bits: int = 45) -> Expr:
    """Return Expr for adding given bit."""
    current = get_expr_expr(num, "^")
    if num == 0:
        return current  # No carry for the least significant bit
    carry = find_last_carry_expr(min(num, max_bits))
    if num >= max_bits:
        return carry
    return Expr(carry, current, Op.XOR)


# z00 =      (x00 ^ y00)
# z01 =     ((x00 & y00) ^ (x01 ^ y01))
# z02 =   (((                         ) | (x01 & y01)) ^ (x02 ^ y02))
#            (x00 & y00) & (x01 ^ y01)
# z03 = ((((((x00 & y00) & (x01 ^ y01)) | (x01 & y01)) & (x02 ^ y02)) | (x02 & y02)) ^ (x03 ^ y03))


def simulate_system(
    wire_states: dict[str, int],
    logic_map: dict[str, Expr],
) -> int:
    """Simulate logic system given wire states and logic map. Return result number."""
    unhandled: set[str] = set(logic_map)
    ticks = 20
    while unhandled:
        found = False
        for result_wire in tuple(unhandled):
            expr = logic_map[result_wire]
            value = expr.calculate_value(wire_states)
            if value is None:
                continue
            wire_states[result_wire] = value
            unhandled.remove(result_wire)
            found = True
        if found:
            ticks = 20
        else:
            ticks -= 1
            if ticks <= 0:
                raise ValueError(unhandled)

    z_value = 0
    z_wires = sorted(
        (wire for wire in wire_states if wire.startswith("z")),
        reverse=True,
    )
    for z_wire in z_wires:
        z_value <<= 1
        z_value |= wire_states[z_wire]
    return z_value


def swap_wires(
    swap: tuple[str, str],
    logic_map: dict[str, Expr],
) -> dict[str, Expr]:
    """Swap a given pair of wires in logic system. Return new logic map with swapped wires."""
    new_logic_map = {
        result: expr
        for result, expr in logic_map.items()
        if result not in swap
    }
    left, right = swap
    new_logic_map[left] = logic_map[right]
    new_logic_map[right] = logic_map[left]
    return new_logic_map


def swap_wires_set(
    to_swap: tuple[
        tuple[str, str],
        tuple[str, str],
        tuple[str, str],
        tuple[str, str],
    ],
    logic_map: dict[str, Expr],
) -> dict[str, Expr]:
    """Return new logic map after swapping four wires."""
    for swap in to_swap:
        logic_map = swap_wires(swap, logic_map)
    return logic_map


def run() -> None:
    """Run program."""
    data = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
    data = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
    data_file = Path(__file__).absolute().parent / "day24.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    wire_states: dict[str, int] = {}
    gen = iter(data.splitlines())
    for line in gen:
        if not line:
            break
        wire_name, wire_value = line.split(": ", 1)
        wire_states[wire_name] = int(wire_value)

    logic_map: dict[str, Expr] = {}
    for line in gen:
        raw_expr, stored_as = line.split(" -> ", 1)
        logic_map[stored_as] = Expr.from_string(raw_expr)

    z_value = simulate_system(wire_states, logic_map)
    print(f"{z_value:b}")
    print(f"{z_value = }")

    swaps = (
        ("z07", "bjm"),
        ("z13", "hsw"),
        ("z18", "skf"),
        ("wkr", "nvr"),
    )
    new_logic_map = swap_wires_set(
        swaps,
        logic_map,
    )

    # Find full equasion for z wires
    expr_map = {
        expr: result_wire for result_wire, expr in new_logic_map.items()
    }
    found = True
    while found:
        found = False
        for expr, result_wire in tuple(expr_map.items()):
            if expr not in expr_map:
                continue
            requirements = False
            for input_name in expr[:2]:
                if input_name in expr_map.values():
                    requirements = True
                    break
            if requirements:
                continue
            # del expr_map[expr]
            for use_expr, use_result_wire in tuple(expr_map.items()):
                del expr_map[use_expr]
                for idx, used_wire in enumerate(use_expr[:2]):
                    if used_wire == result_wire:
                        found = True
                        replace_data = {use_expr._fields[idx]: expr.as_code()}
                        # incompatible type "**dict[str, str]"; expected "Op"
                        use_expr = use_expr._replace(
                            **replace_data,  # type: ignore[arg-type]
                        )
                expr_map[use_expr] = use_result_wire

    # Check logic system to make sure full equasions for z wires match
    failure = False
    rev_expr_map = {
        result_wire: expr for expr, result_wire in expr_map.items()
    }
    for z_wire in sorted(
        (wire for wire in wire_states if wire.startswith("z")),
        reverse=False,
    ):
        expr_code = rev_expr_map[z_wire].as_code()
        num = int(z_wire.removeprefix("z"))
        add = find_add(num)
        if expr_code != add:
            print(f"[T]{z_wire} = {expr_code}")
            print(f"[R]{z_wire} = {add}")
            print("different!")
            failure = True
            break
    # If different
    if failure:
        # Find correct full add expression for incorrect bit
        expr = find_add_expr(num)
        # Go down the rabbit hole of expressions and find innermost layer
        ups = []
        while True:
            up = expr
            if isinstance(expr[0], str):
                break
            ups.append(up)
            expr = expr[0]
        rev_logic_map = {
            expr: result_wire for result_wire, expr in new_logic_map.items()
        }

        # Print out existing wire map
        for result_wire in logic_map:
            print(f"{result_wire} = {logic_map[result_wire].as_code()}")
        print("####################")

        # While not at topmost layer yet
        while ups:
            # Find what name current expression (left side) has
            try:
                value = rev_logic_map[expr]
            except KeyError:
                print(f"{expr} not found")
                break

            # Rebuild expression from next layer up
            new_expr = ups.pop()
            two = new_expr.two
            assert isinstance(two, Expr)
            # Find name of right side of expression
            try:
                right = rev_logic_map[two]
            except KeyError:
                print(f"{new_expr[1]} not found")
                break
            # Make sure is in order
            one, two = sorted((value, right))
            expr = Expr(one, two, new_expr[2])
            print(f"{rev_logic_map[expr]} = {expr.as_code()}")
        print(f"{expr = }")
        print(f"{logic_map[z_wire] = }")
    else:
        # Otherwise, all z wires correct!
        items: list[str] = []
        for swap in swaps:
            items.extend(swap)
        print(",".join(sorted(items)))


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
