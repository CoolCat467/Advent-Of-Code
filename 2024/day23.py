"""Advent of Code 2024 Day 23."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 23
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

__title__ = "Advent of Code 2024 Day 23"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def find_triangles_gen(
    connections: dict[str, set[str]],
) -> Generator[tuple[str, str, str], None, None]:
    """Find sets of three interconnected computers."""
    # Created with help from ChatGPT-4o mini

    # Iterate through each computer and its connections
    for computer, connected in connections.items():
        connected_tuple = tuple(connected)
        # Check each pair of neighbors
        for i, neighbor in enumerate(connected_tuple):
            for neighbor2 in connected_tuple[i:]:
                # Check if the two neighbors are connected
                if neighbor2 in connections[neighbor]:
                    # If they are connected, we found a triangle
                    t1, t2, t3 = sorted((computer, neighbor, neighbor2))
                    yield (t1, t2, t3)


def bron_kerbosch(
    r: set[str],
    p: set[str],
    x: set[str],
    connections: dict[str, set[str]],
) -> list[set[str]]:
    """Bron-Kerbosch algorithm to find all maximal cliques (fully connected sets).

    r: the current clique being built
    p: potential nodes to add to the clique
    x: nodes that have already been considered and should not be added
    """
    # Created with help from ChatGPT-4o mini

    # If no potential nodes and nothing not to add,
    # then maximal chique is currently build one.
    if not p and not x:
        return [r]

    cliques = []
    for v in p.copy():
        new_r = r | {v}
        new_p = p & connections[v]
        new_x = x & connections[v]
        cliques.extend(bron_kerbosch(new_r, new_p, new_x, connections))
        p.remove(v)
        x.add(v)

    return cliques


def find_largest_clique(
    connections: dict[str, set[str]],
) -> set[str]:
    """Return the largest clique in the graph."""
    # Created with help from ChatGPT-4o mini

    all_nodes = set(connections)
    cliques = bron_kerbosch(set(), all_nodes, set(), connections)
    return max(cliques, key=len, default=set())


def run() -> None:
    """Run program."""
    data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    data_file = Path(__file__).absolute().parent / "day23.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    # Build graph of connections
    connections: dict[str, set[str]] = {}
    for line in data.splitlines():
        left, right = line.split("-", 1)

        connections.setdefault(left, set()).add(right)

        connections.setdefault(right, set()).add(left)

    ##triangles = find_triangles(connections)
    ##for triangle in triangles:
    ##    print(triangle)
    ##print(f'{len(triangles) = }')

    # Find all triangles that contain nodes with "t" in their name
    start_t_triangles: set[tuple[str, str, str]] = set()
    for triangle in find_triangles_gen(connections):
        for computer_name in triangle:
            if computer_name.startswith("t"):
                start_t_triangles.add(triangle)
    ##for triangle in start_t_triangles:
    ##    print(triangle)
    print(f"{len(start_t_triangles) = }")

    # Find the largest clique (fully connected set) of nodes in graph
    largest = find_largest_clique(connections)
    print(f"{len(largest) = }")
    print(",".join(sorted(largest)))


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
