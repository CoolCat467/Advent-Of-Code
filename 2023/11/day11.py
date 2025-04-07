"""Advent of Code 2023 Day 11."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 11"
__author__ = "CoolCat467"
__version__ = "0.0.0"


def display(galaxies: list[tuple[int, tuple[int, ...]]]) -> None:
    """Display galaxies."""
    width = 0
    height = 0
    for y, x_pos in galaxies:
        for x in x_pos:
            width = max(width, x)
        height = max(height, y)
    width += 1
    height += 1

    lines = []
    mapping = dict(galaxies)
    for y in range(height):
        if y not in mapping:
            lines.append("." * width)
            continue
        last_x = 0
        current = ""
        for x_pos in mapping[y]:
            current += "." * (x_pos - last_x) + "#"
            last_x = x_pos
        lines.append(current.ljust(width, "."))
    print("\n".join(lines))


def process(input_: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    lines = input_.splitlines()
    # height = len(lines)
    # width = len(lines[0])

    horiz_stretched: list[tuple[int, tuple[int, ...]]] = []
    y = 0
    columns_with_galaxies: set[int] = set()
    for line in lines:
        x_pos = []
        for x, char in enumerate(line):
            if char == ".":
                continue
            x_pos.append(x)
            ##            bisect.insort(columns_with_galaxies, x)
            columns_with_galaxies.add(x)
        if not x_pos:
            y += 2
            ##            y += 1
            continue
        horiz_stretched.append((y, tuple(x_pos)))
        y += 1
    stretched: list[tuple[int, tuple[int, ...]]] = []
    for y, x_values in horiz_stretched:
        x_pos = []
        for ox in x_values:
            x = 0
            ##            index = bisect.bisect(columns_with_galaxies, x)
            for idx in range(ox):
                if idx not in columns_with_galaxies:
                    x += 1
            x_pos.append(ox + x)
        stretched.append((y, tuple(x_pos)))
    display(stretched)

    points = []
    for y, x_values in stretched:
        for x in x_values:
            points.append((x, y))

    connections_left: dict[int, int] = dict.fromkeys(range(len(points)), 2)
    connection_distances: dict[tuple[int, int], int] = {}
    sum_path = 0
    for index, point in enumerate(points):
        x, y = point
        distances: dict[int, list[int]] = {}
        for index2, point2 in enumerate(points):
            if index == index2:
                continue
            if index not in connections_left:
                continue
            if index2 not in connections_left:
                continue
            if (index, index2) in connection_distances:
                continue
            if (index2, index) in connection_distances:
                continue
            x2, y2 = point2
            dx = max(x, x2) - min(x, x2)
            dy = max(y, y2) - min(y, y2)
            distance = dx + dy
            distances.setdefault(distance, []).append(index2)
        if not distances:
            continue
        added = 0
        while added != 2:
            min_distance = min(distances)
            min_points = distances[min_distance]
            for mp in min_points:
                connection_distances[(index, mp)] = min_distance
                connection_distances[(mp, index)] = min_distance
                sum_path += min_distance
                connections_left[mp] -= 1
                connections_left[index] -= 1
                if connections_left[index] <= 0:
                    del connections_left[index]
                    added = 2
                    break
                if connections_left[mp] <= 0:
                    del connections_left[mp]
                added += 1
            del distances[min_distance]

    print(f"{len(connection_distances) = }")
    for point, distance in connection_distances.items():
        x, y = point
        print(f"{x+1} to {y+1}: {distance}")

    return sum_path, 0


def run() -> None:
    """Print answer."""
    input_ = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    ##    with open("day11.txt", encoding="utf-8") as file:
    ##        input_ = file.read()
    result = process(input_)
    print(f"process(input_) = {result}")
    assert result[0] == 374


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
