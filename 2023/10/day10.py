"""Advent of Code 2023 Day 10."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 10"
__author__ = "CoolCat467"
__version__ = "0.0.0"

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


def get_outline(
    line_no: int,
    column_no: int,
) -> Generator[tuple[int, int], None, None]:
    """Yield outline (line, column) positions given match (line number, start column, and end column)."""
    for line in range(line_no - 1, line_no + 2):
        for col in range(column_no - 1, column_no + 2):
            if line == line_no and col == column_no:
                continue
            if line != line_no and col != column_no:
                continue
            yield (line, col)


def cancel_out_of_bounds(
    gen: Generator[tuple[int, int], None, None],
    end_x: int,
    end_y: int,
    start_x: int = 0,
    start_y: int = 0,
) -> Generator[tuple[int, int], None, None]:
    """Ignore positions that are out of bounds."""
    for x, y in gen:
        if x < start_x or x >= end_x:
            continue
        if y < start_y or y >= end_y:
            continue
        yield (x, y)


def outline_bounds(
    line_no: int,
    column_no: int,
    rect: tuple[int, int] | tuple[int, int, int, int],
) -> Generator[tuple[int, int], None, None]:
    """Yield outline coordinates and ignore out of bounds coordinates."""
    yield from cancel_out_of_bounds(
        get_outline(
            line_no,
            column_no,
        ),
        *rect,
    )


def continues(tile: str) -> tuple[bool, bool, bool, bool]:
    """Return North, East, South, West boolean tuples."""
    # North East South West
    if tile == "S":  # All
        return (True, True, True, True)
    if tile == "|":  # North South
        return (True, False, True, False)
    if tile == "-":  # East West
        return (False, True, False, True)
    if tile == "L":  # North East
        return (True, True, False, False)
    if tile == "J":  # North West
        return (True, False, False, True)
    if tile == "F":  # South East
        return (False, True, True, False)
    if tile == "7":  # South West
        return (False, False, True, True)
    return (False, False, False, False)


def valid_continues(
    start_pos: tuple[int, int],
    lines: list[str],
    bounds: tuple[int, int] | tuple[int, int, int, int],
) -> Generator[tuple[int, int], None, None]:
    """Yield valid continue positions."""
    sx, sy = start_pos
    start_tile = lines[sy][sx]
    ##    print(F'{start_tile = }')
    start_connect = continues(start_tile)
    for x, y in outline_bounds(*start_pos, bounds):
        # ox = sx - x
        oy = sy - y
        if lines[y][x] == ".":
            continue
        outline = continues(lines[y][x])
        ##        print()
        ##        print(
        ##            make_graphic(
        ##                {start_tile: {start_pos}, lines[y][x]: {(x, y)}},
        ##                bounds,
        ##            ),
        ##        )
        horizontal = x != sx
        ##        print(f'{horizontal = }')
        range_ = (1, 5, 2) if horizontal else (0, 4, 2)
        for index in range(*range_):
            if not start_connect[index]:
                continue
            ##            print(f"{index = }")
            # 0 North
            # 1 East
            # 2 South
            # 3 West
            ##            match = (4 - index) % 4
            match = {0: 2, 2: 0, 1: 3, 3: 1}[index]
            if oy and start_tile in {"F", "7"}:
                if oy > 0 and lines[y][x] in {"F", "7"}:
                    continue
                if oy < 0 and lines[y][x] in {"J", "L"}:
                    continue
            if oy and start_tile in {"J", "L"}:
                if oy < 0 and lines[y][x] in {"F", "7"}:
                    continue
                if oy > 0 and lines[y][x] in {"J", "L"}:
                    continue
            ##            print(f"{match = }")
            if not outline[match]:
                continue
            ##            print("yes")

            yield (x, y)
            break


def furthest_from(
    start_pos: tuple[int, int],
    lines: list[str],
    width: int,
) -> dict[int, Iterable[tuple[int, int]]]:
    """Return dict of largest distances."""
    bounds = (width, len(lines))
    directions = set(valid_continues(start_pos, lines, bounds))
    visited: set[tuple[int, int]] = {start_pos}
    distances: dict[int, Iterable[tuple[int, int]]] = {}
    distances[0] = {start_pos}
    steps = 1
    ##    print(f"{directions = }")
    while directions:
        distances[steps] = directions
        visited |= directions
        next_directions = set()
        for pos in directions:
            next_directions |= set(valid_continues(pos, lines, bounds))
        directions = next_directions - visited
        ##        print(next_directions)
        steps += 1
    ##        print(len(directions))

    return distances


def make_graphic(
    distances: dict[int, Iterable[tuple[int, int]]]
    | dict[str, Iterable[tuple[int, int]]],
    bounds: tuple[int, int],
) -> str:
    """Generate graphic given distances table."""
    lines = []
    width, height = bounds
    for _ in range(height):
        lines.append(["." for _ in range(width)])
    for distance, points in distances.items():
        str_dist = str(distance)
        for x, y in points:
            lines[y][x] = str_dist
    return "\n".join("".join(line) for line in lines)


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    lines = text.splitlines()
    width = len(lines[0])
    y = 0
    for y, line in enumerate(lines):  # noqa: B007
        x = line.find("S")
        if x != -1:
            break
    ##    print(f"{width = }")
    ##    print(f"{(x, y)}")

    distances = furthest_from((x, y), lines, width)
    ##    print(make_graphic(distances, (width, len(lines))))

    return 0, max(distances) + 1


def run() -> None:
    """Print answer."""
    input_ = """.....
.S-7.
.|.|.
.L-J.
....."""
    input_ = """.....
.F-7.
.|.|.
.S-J.
....."""
    input_ = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    ##    input_ = """-L|F7
    ##7S-7|
    ##L|7||
    ##-L-J|
    ##L|-JF"""
    with open("day10.txt", encoding="utf-8") as file:
        input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
