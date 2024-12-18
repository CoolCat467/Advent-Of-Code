"""Advent of Code 2024 Day 18."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 18
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

__title__ = "Advent of Code 2024 Day 18"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


# Stolen from 2024 Days 6, 10, and 12
def get_point_edges(
    x: int,
    y: int,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Return edges of given point."""
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )


# Stolen from 2024 Days 10, 12, 14, 15, and 16
def render_map(
    regions: Sequence[tuple[str, Sequence[tuple[int, int]]]],
    w: int,
    h: int,
) -> None:
    """Render map."""
    buffer = ""
    for y in range(h):
        for x in range(w):
            for char, points in regions:
                if (x, y) in points:
                    buffer += char
                    break
            else:
                buffer += "."  # " "
        buffer += "|\n"
    print(buffer)


def render_matrix(
    matrix: dict[tuple[int, int], int],
    width: int,
    height: int,
) -> None:
    """Render matrix."""
    render: dict[int, list[tuple[int, int]]] = {}
    for pos, dist in matrix.items():
        points = render.get(dist, [])
        points.append(pos)
        render[dist] = points
    ##render_map(
    ##    [(str(k) if k < 10 else chr(k + 55), v) for k, v in render.items()],
    ##    width,
    ##    height,
    ##)
    render_map(
        [("O", v) for k, v in render.items()],
        width,
        height,
    )


def calculate_matrix(
    corrupted: tuple[tuple[int, int], ...],
    width: int,
    height: int,
) -> dict[tuple[int, int], int]:
    """Return matrix given corrupted tiles and size."""
    matrix: dict[tuple[int, int], int] = {(0, 0): 0}
    heads: list[tuple[int, int]] = [(0, 0)]
    while heads:
        head = heads.pop()
        new_distance = matrix[head] + 1
        edges = get_point_edges(*head)
        for edge in edges:
            x, y = edge
            if x < 0 or x >= width:
                continue
            if y < 0 or y >= height:
                continue
            if edge in corrupted:
                continue
            old_distance = matrix.get(edge)
            if old_distance is None or old_distance > new_distance:
                matrix[edge] = new_distance
                heads.append(edge)
    return matrix


def update_matrix(
    matrix: dict[tuple[int, int], int],
    remove_point: tuple[int, int],
    corrupted: tuple[tuple[int, int], ...],
    width: int,
    height: int,
) -> bool:
    """Update given matrix given the corrupted tile that was removed. Return if valid path to end exists."""
    assert remove_point not in corrupted
    heads: list[tuple[int, int]] = []
    for edge in get_point_edges(*remove_point):
        if matrix.get(edge) is not None:
            heads.append(edge)
    while heads:
        head = heads.pop()
        new_distance = matrix[head] + 1
        edges = get_point_edges(*head)
        for edge in edges:
            x, y = edge
            if x < 0 or x >= width:
                continue
            if y < 0 or y >= height:
                continue
            if edge in corrupted:
                continue
            old_distance = matrix.get(edge)
            if old_distance is None or old_distance > new_distance:
                matrix[edge] = new_distance
                heads.append(edge)

    return matrix.get((width - 1, height - 1)) is not None


def run() -> None:
    """Run program."""
    data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    data_file = Path(__file__).absolute().parent / "day18.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    bytes_: list[tuple[int, int]] = []
    width = 0
    height = 0
    for line in data.splitlines():
        x, y = map(int, line.split(",", 1))
        width = max(x, width)
        height = max(y, height)
        bytes_.append((x, y))
    width += 1
    height += 1
    original = tuple(bytes_)

    ##width, height = (7, 7)
    ##fall = 12
    fall = 1024

    index = len(original) - 1
    matrix = calculate_matrix(original, width, height)
    for index, remove_point in reversed(tuple(enumerate(original))):
        if update_matrix(
            matrix,
            remove_point,
            original[:index],
            width,
            height,
        ):
            render_matrix(matrix, width, height)
            print(f"{index = }")
            print(f"{remove_point = }")
            print("Part 2: " + ",".join(map(str, remove_point)))
            break
    for _ in range(index - fall):
        remove_point = original[index]
        index -= 1
        update_matrix(matrix, remove_point, original[:index], width, height)
    path = matrix[(width - 1, height - 1)]
    print(f"Part 1: {path = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
