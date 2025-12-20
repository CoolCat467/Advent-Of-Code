#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 11

"Advent of Code 2022 Day 11."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 11"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import dataclasses
import io
from collections import deque
from math import lcm
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclasses.dataclass(slots=True)
class Monkey:
    "Monkey class."  # noqa: D300

    number: int
    start: tuple[int, ...]
    operator: Callable[[int], int]
    div: int
    which: tuple[int, int]


def parse_op(command: str) -> Callable[[int], int]:
    "Parse command into callable function."  # noqa: D300
    command = command.removeprefix("new = old ")
    operator, value = command.split(" ", 1)
    if value.isdigit():
        digit = int(value)
        if operator == "+":
            return lambda x: x + digit
        if operator == "*":
            return lambda x: x * digit
    elif value == "old":
        if operator == "+":
            return lambda x: x + x
        if operator == "*":
            return lambda x: x * x
    raise ValueError(f"Unhandled {command = }")


def get_monkey(data: str) -> Monkey:
    "Parse monkey data into a Monkey object."  # noqa: D300
    lines = [l.strip() for l in data.splitlines()]  # noqa: E741
    number = int(lines[0].removeprefix("Monkey ").removesuffix(":"))
    start = tuple(
        map(int, lines[1].removeprefix("Starting items: ").split(", ")),
    )
    operator = parse_op(lines[2].removeprefix("Operation: "))
    div = int(lines[3].removeprefix("Test: divisible by "))
    if_true = int(lines[4].removeprefix("If true: throw to monkey "))
    if_false = int(lines[5].removeprefix("If false: throw to monkey "))
    which = (if_false, if_true)
    return Monkey(number, start, operator, div, which)


class MonkeyProcessor:
    "Bad monkey processor that can't handle super long simulations."  # noqa: D300

    __slots__ = ("counts", "do_div", "held", "lcm", "monkeys")
    debug = False

    def __init__(  # noqa: D107
        self,
        monkeys: list[Monkey],
        do_div: bool = True,
    ) -> None:
        self.monkeys = {m.number: m for m in monkeys}
        self.held = {m.number: deque(m.start) for m in monkeys}
        self.counts = {m.number: 0 for m in monkeys}
        self.do_div = do_div

        self.lcm = lcm(*(m.div for m in monkeys))

    @classmethod
    def log(cls, msg: str) -> None:
        "Log a message."  # noqa: D300
        if cls.debug:
            print(msg)

    def throw(self, item: int, recipient: int) -> None:
        "Trow item to recipient monkey."  # noqa: D300
        self.held[recipient].append(item)

    def inspect(self, mid: int, item: int) -> None:
        "Monkey mid inspects and throws item."  # noqa: D300
        self.log(f"  Monkey inspects an item with a worry level of {item}.")
        worry = self.monkeys[mid].operator(item)
        self.log(f"    Worry level is now {worry}.")
        if self.do_div:
            worry //= 3
            self.log(
                f"    Monkey gets bored with item. Worry level is divided by 3 to {worry}.",
            )
        worry %= self.lcm
        self.log(
            f"    Worry is now {worry} from modulus {self.lcm} to keep values low, has no effect on inspect counts",
        )
        which = int(worry % self.monkeys[mid].div == 0)

        may_not = (" not", "")[which]
        self.log(
            f"    Current worry level is{may_not} divisible by {self.monkeys[mid].div}.",
        )
        recipient = self.monkeys[mid].which[which]
        self.log(
            f"    Item with worry level {worry} is thrown to monkey {recipient}.",
        )
        self.throw(worry, recipient)

        self.counts[mid] += 1

    def turn(self, mid: int) -> None:
        "Perform turn for the given monkey inspecting items."  # noqa: D300
        self.log(f"Monkey {mid}:")
        for _ in range(len(self.held[mid])):
            item = self.held[mid].popleft()
            self.inspect(mid, item)

    def round(self) -> None:
        "Perform one round of monkeys taking turns."  # noqa: D300
        for mid in self.monkeys:
            self.turn(mid)
        for mid, items in self.held.items():
            self.log(f"Monkey {mid}: {', '.join(map(str, items))}")
        self.log("-" * 20)


def part_one(monkeys: list[Monkey]) -> int:
    "Find level of monkey business after 20 round."  # noqa: D300
    processor = MonkeyProcessor(monkeys)
    for _ in range(20):
        processor.round()
    top = sorted(processor.counts.values(), reverse=True)
    ##    print(top)
    one, two = top[:2]
    return one * two


def part_two(monkeys: list[Monkey]) -> int:
    "Find level of monkey business after 10000 rounds and no floor div 3."  # noqa: D300
    processor = MonkeyProcessor(monkeys, False)
    for _ in range(10000):
        processor.round()
    top = sorted(processor.counts.values(), reverse=True)
    ##    print(top)
    one, two = top[:2]
    return one * two


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

    file = io.StringIO(test_data)
    ##    file = open('day11.txt', encoding='utf-8')

    monkeys: list[Monkey] = []

    buffer = ""
    for line in file:
        if line == "\n":
            monkeys.append(get_monkey(buffer))
            buffer = ""
        else:
            buffer += line
    monkeys.append(get_monkey(buffer))

    file.close()

    ##    assert part_one(monkeys) == 10605, "code change is bad"
    print(f"{part_one(monkeys) = }")
    print(f"{part_two(monkeys) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
