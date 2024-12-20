#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 1

"Advent of Code 2022 Day 1."  # noqa: D300

# Programmed by CoolCat467

# Today experimenting with asynchronous generators
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 1"
__author__ = "CoolCat467"
__version__ = "0.0.0"


import io
from typing import TYPE_CHECKING

import trio

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


async def handler() -> AsyncGenerator[list[int], str | None]:
    "File handler."  # noqa: D300
    maxes: dict[int, int] = {}
    cur_max = 0
    cur_total = 0
    cur_elf = 0
    while True:
        new = yield sorted(maxes.values(), reverse=True)[:3]
        if not new:
            if cur_total > cur_max:
                cur_max = cur_total
            maxes[cur_elf] = cur_total
            cur_total = 0
            cur_elf += 1
        else:
            cur_total += int(new)


async def async_run() -> None:
    "Asynchronous entry point."  # noqa: D300
    test_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    reader = handler()
    await reader.asend(None)
    max_values = [0, 0, 0]
    file = trio.wrap_file(io.StringIO(test_data))
    ##    file = await trio.open_file('day1.txt', encoding='utf-8')
    async for line in file:
        max_values = await reader.asend(line.strip())
    await file.aclose()
    max_values = await anext(reader)
    print(f"{max_values[0] = }")
    print(f"{sum(max_values) = }")


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    trio.run(async_run)


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
