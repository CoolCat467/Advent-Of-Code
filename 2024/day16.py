"""Advent of Code 2024 Day 16."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 16
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

__title__ = "Advent of Code 2024 Day 16"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING, Final, NamedTuple, Self

from vector import Vector2

if TYPE_CHECKING:
    from collections.abc import Collection


DIR_LOOKUP: Final = {
    0: Vector2(0, -1),
    1: Vector2(1, 0),
    2: Vector2(0, 1),
    3: Vector2(-1, 0),
}


def vec2_to_int(vec: Vector2) -> tuple[int, int]:
    """Help mypy understand Vector2 is same as tuple[int, int]."""
    x, y = vec
    return int(x), int(y)


class InProgressSolve(NamedTuple):
    """In-progress solve status."""

    direction: int
    score: int
    visited: int

    def forward(self, pos: Vector2) -> tuple[Vector2, Self]:
        """Return forward position and associated solve status."""
        delta: Vector2
        div, mod = divmod(self.direction, 2)
        if mod == 0:
            delta = Vector2(0, div * 2 - 1)
        else:
            delta = Vector2(1 - (div * 2), 0)
        return (
            pos + delta,
            self._replace(score=self.score + 1, visited=self.visited + 1),
        )

    def turn_left(self) -> Self:
        """Return new solve status after turning left."""
        return self._replace(
            direction=(self.direction + 3) % 4,
            score=self.score + 1000,
        )

    def turn_right(self) -> Self:
        """Return new solve status after turning right."""
        return self._replace(
            direction=(self.direction + 1) % 4,
            score=self.score + 1000,
        )


class Map(NamedTuple):
    """Map Object."""

    walls: frozenset[tuple[int, int]]
    start: Vector2
    end: Vector2

    @classmethod
    def read_map(cls, map_data: list[str]) -> Self:
        """Return new Map object from map data."""
        walls: set[tuple[int, int]] = set()
        start = Vector2(0, 0)
        end = Vector2(0, 0)

        for y, line in enumerate(map_data):
            for x, char in enumerate(line):
                if char == "S":
                    start = Vector2(x, y)
                    continue
                if char == "#":
                    walls.add((x, y))
                    continue
                if char == "E":
                    end = Vector2(x, y)
                    continue
                if char == ".":
                    continue
                raise ValueError(char)
        return cls(
            frozenset(walls),
            start,
            end,
        )

    def render_map(
        self,
        visited: Collection[tuple[int, int]] | None = None,
    ) -> None:
        """Render and print robot map to console."""
        # Find dimensions
        end_x, end_y = 0, 0
        for x, y in self.walls:
            end_x = max(end_x, x)
            end_y = max(end_y, y)

        # Type checker convinced Vector2 != tuple[int, int]
        start = vec2_to_int(self.start)
        end = vec2_to_int(self.end)

        if visited is None:
            visited = set()

        # Will print out all at once for lag purposes
        buffer = ""
        for y in range(end_y + 1):
            for x in range(end_x + 1):
                if (x, y) == start:
                    buffer += "S"
                    continue
                if (x, y) == end:
                    buffer += "E"
                    continue
                if (x, y) in self.walls:
                    buffer += "█"  # "#"
                    continue
                if (x, y) in visited:
                    buffer += "O"
                    continue
                buffer += " "  # "."
            buffer += "\n"
        print(buffer)

    def solve(self) -> tuple[int, dict[tuple[int, int], InProgressSolve]]:
        """Solve and return min score and map of visited points."""
        # Find dimensions
        end_x, end_y = 0, 0
        for x, y in self.walls:
            end_x = max(end_x, x)
            end_y = max(end_y, y)
        path_points = {
            (x, y) for x in range(end_x + 1) for y in range(end_y + 1)
        } - self.walls

        visited: set[tuple[int, int]] = set()
        path: dict[tuple[int, int], InProgressSolve] = {
            self.start: InProgressSolve(1, 0, 0),
        }

        def add_forward(solve, cur_pos):
            new_pos, new_solve = solve.forward(cur_pos)
            if new_pos not in self.walls:
                old_solve = path.get(new_pos)
                if old_solve is not None:
                    if old_solve.score > new_solve.score:
                        path[new_pos] = new_solve
                else:
                    path[new_pos] = new_solve

        ##        ticks = 0
        path_tiles = len(path_points)
        for _ in range(path_tiles + path_tiles // 2):
            for cur_pos, solve in tuple(path.items()):
                if cur_pos in visited:
                    continue
                add_forward(solve, cur_pos)
                add_forward(solve.turn_left(), cur_pos)
                add_forward(solve.turn_right(), cur_pos)
        ##                visited.add(cur_pos)
        ##            if self.end in path:
        ##            if len(path) >= path_tiles:
        ##                assert self.end in path
        ##                ticks += 1
        ##                if ticks > 40:# 70:
        ##                    return path[self.end].score, path
        ##                new_pos, new_solve = solve.forward(cur_pos)
        ##                if new_pos not in self.walls:
        ##                    if new_pos in path:
        ##                        old_solve = path[new_pos]
        ##                        if old_solve.score > new_solve.score:
        ##                            path[new_pos] = new_solve
        ##                    else:
        ##                        path[new_pos] = new_solve
        ##        print(f'{sorted(path.items(), key=lambda x: x[1].score) = }')
        ##        assert self.end in path
        return path[self.end].score, path


def find_best_path_counts(
    path: dict[tuple[int, int], InProgressSolve],
    start: tuple[int, int],
    end: tuple[int, int],
) -> set[tuple[int, int]]:
    """Return tiles used in best paths."""
    current = {end}

    points: set[tuple[int, int]] = set()
    show = False
    while start not in current:
        next_ = set()
        for item in current:
            if show:
                print(f"{item = }")
            points.add(item)
            cur_solve = path[item]
            ##            next_score = [cur_solve.score - 1, cur_solve.score - 1001]#, cur_solve.score - 2001]
            for delta in DIR_LOOKUP.values():
                key = item - delta
                if key in points:
                    continue
                solve = path.get(key)
                if solve is None:
                    continue
                ##                if solve.score in next_score:
                ##                    print(f'{next_score.index(solve.score) = }')
                if solve.score < cur_solve.score:
                    ##                if solve.visited < cur_solve.visited:
                    # solve.visited == (cur_solve.visited - 1) and
                    next_.add(key)
                elif solve.visited < cur_solve.visited:
                    next_.add(key)
        ##        print(f'{len(next_) = }')
        ##        print(f"{next_ = }")
        ##        if not next_:
        ##            print("out of points!")
        ##            print(f'{current = }')
        ##            for delta in DIR_LOOKUP.values():
        ##                key = item - delta
        ##                if key in points:
        ##                    continue
        ##                solve = path.get(key)
        ##                if solve is None:
        ##                    continue
        ##                print(f'{key} {cur_solve.score} {solve.score}')
        ####                if solve.score <= cur_solve.score:
        ##                next_.add(key)
        ##            show = True
        if not next_:
            print("still out of points!")
            break
        current = next_
    if start in current:
        points.add(start)
    print(f"{start in current = }")
    return points


def run() -> None:
    """Run program."""
    data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    data = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    data_file = Path(__file__).absolute().parent / "day16.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    map_data = data.splitlines()

    # Read map
    map_ = Map.read_map(map_data)
    ##    map_.render_map()

    score, path = map_.solve()
    print(f"{score = }")
    # 119476 too high
    # 109496
    ##    print("caching")
    ##    with open("day16_path.txt", "w", encoding="utf-8") as fp:
    ##        json.dump({"_".join(map(str, k)):v for k, v in path.items()}, fp)
    ##    print("load from cache")
    ##    path = {}
    ##    with open("day16_path.txt", "r", encoding="utf-8") as fp:
    ##        for key, value in json.load(fp).items():
    ##            path[Vector2.from_iter(map(int, key.split("_")))] = InProgressSolve(*value)
    points = find_best_path_counts(path, map_.start, map_.end)
    ##    points = find_best_path_counts(path, map_.end, map_.start)

    map_.render_map(points)
    # 592 too high
    # 568  too high
    # 565 too high
    # 552 ?
    # 539 too low
    # 537 too low

    print(f"{len(points) = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
