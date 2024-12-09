"""Advent of Code 2024 Day 8."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 8
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

__title__ = "Advent of Code 2024 Day 8"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Collection,
        Generator,
        Iterable,
        Mapping,
    )

Node = tuple[int, int]


def node_distance(one: Node, two: Node) -> Node:
    """Return subtraction of two - one."""
    x1, y1 = one
    x2, y2 = two
    return (x2 - x1), (y2 - y1)


def node_add(one: Node, two: Node) -> Node:
    """Return addition of one node with another."""
    x1, y1 = one
    x2, y2 = two
    return (x1 + x2), (y1 + y2)


def get_aninode(one: Node, two: Node) -> Node:
    """Return antinodes pair."""
    return node_add(two, node_distance(one, two))


def is_out_of_bounds(x: int, y: int, w: int, h: int) -> bool:
    """Return if given position is out of bounds."""
    return (x < 0 or x >= w) or (y < 0 or y >= h)


def get_group_antinodes(
    group: Iterable[Node],
    width: int,
    height: int,
) -> set[Node]:
    """Return group antinodes."""
    antinodes: set[Node] = set()
    for index, one in enumerate(group):
        for index2, two in enumerate(group):
            if index == index2:
                continue
            antinode = get_aninode(one, two)
            if not is_out_of_bounds(*antinode, width, height):
                antinodes.add(antinode)
    return antinodes


def yield_antinodes(
    one: Node,
    two: Node,
    width: int,
    height: int,
) -> Generator[Node, None, None]:
    """Yield antinodes until out of bounds."""
    delta = node_distance(one, two)
    antinode = two  # node_add(two, delta)
    while not is_out_of_bounds(*antinode, width, height):
        yield antinode
        antinode = node_add(antinode, delta)


def get_group_antinode_harmonics(
    group: Iterable[Node],
    width: int,
    height: int,
) -> set[Node]:
    """Return group antinodes (including harmonic frequencies)."""
    antinodes: set[Node] = set()
    for index, one in enumerate(group):
        for index2, two in enumerate(group):
            if index == index2:
                continue
            for antinode in yield_antinodes(one, two, width, height):
                antinodes.add(antinode)
    return antinodes


def render_nodes(
    nodes: Mapping[str, Collection[Node]],
    map_size: tuple[int, int],
) -> None:
    """Print out map with nodes."""
    width, height = map_size
    buffer = ""
    for y in range(height):
        for x in range(width):
            for char, positions in nodes.items():
                if (x, y) in positions:
                    buffer += char
                    break
            else:
                buffer += "."
        buffer += "\n"
    print(buffer)


def run() -> None:
    """Run program."""
    ##    data = """T.........
    ##...T......
    ##.T........
    ##..........
    ##..........
    ##..........
    ##..........
    ##..........
    ##..........
    ##.........."""
    data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    data_file = Path(__file__).absolute().parent / "day8.txt"
    if data_file.exists():
        data = data_file.read_text()

    nodes: dict[str, set[Node]] = {}

    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == ".":
                continue
            entry = nodes.get(char)
            if entry is None:
                nodes[char] = {(x, y)}
            else:
                entry.add((x, y))
    width, height = (x + 1, y + 1)

    antinodes: set[Node] = set()
    for node_set in nodes.values():
        antinode_set = get_group_antinodes(node_set, width, height)
        antinodes |= antinode_set
    ##del nodes["#"]
    ##nodes["#"] = antinodes
    ##render_nodes(nodes, (width, height))
    print(f"{len(antinodes) = }")

    antinodes.clear()
    for node_set in nodes.values():
        antinode_set = get_group_antinode_harmonics(node_set, width, height)
        antinodes |= antinode_set
    ##nodes["#"] = antinodes
    ##render_nodes(nodes, (width, height))
    print(f"{len(antinodes) = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
