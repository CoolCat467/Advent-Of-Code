"""Advent of Code 2024 Day 15."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 15
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

__title__ = "Advent of Code 2024 Day 15"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path
from typing import TYPE_CHECKING, Final, NamedTuple, Self

from vector import Vector2

if TYPE_CHECKING:
    from collections.abc import Collection, Generator


INSTRUCTION_LOOKUP: Final = {
    "^": Vector2(0, -1),
    ">": Vector2(1, 0),
    "v": Vector2(0, 1),
    "<": Vector2(-1, 0),
}


def vec2_to_int(vec: Vector2) -> tuple[int, int]:
    """Help mypy understand Vector2 is same as tuple[int, int]."""
    x, y = vec
    return int(x), int(y)


class Map(NamedTuple):
    """Map Object."""

    boxes: frozenset[tuple[int, int]]
    walls: frozenset[tuple[int, int]]
    robot: Vector2

    @classmethod
    def read_map(cls, map_data: list[str]) -> Self:
        """Return new Map object from map data."""
        boxes: set[tuple[int, int]] = set()
        walls: set[tuple[int, int]] = set()
        robot = Vector2(0, 0)

        for y, line in enumerate(map_data):
            for x, char in enumerate(line):
                if char == "@":
                    robot = Vector2(x, y)
                    continue
                if char == "#":
                    walls.add((x, y))
                    continue
                if char == "O":
                    boxes.add((x, y))
                    continue
                if char == ".":
                    continue
                raise ValueError(char)
        return cls(
            frozenset(boxes),
            frozenset(walls),
            robot,
        )

    def render_map(self) -> None:
        """Render and print robot map to console."""
        # Find dimensions
        end_x, end_y = 0, 0
        for x, y in self.walls:
            end_x = max(end_x, x)
            end_y = max(end_y, y)

        # Type checker convinced Vector2 != tuple[int, int]
        robot = vec2_to_int(self.robot)

        # Will print out all at once for lag purposes
        buffer = ""
        for y in range(end_y + 1):
            for x in range(end_x + 1):
                if (x, y) == robot:
                    buffer += "@"
                    continue
                if (x, y) in self.walls:
                    buffer += "#"
                    continue
                if (x, y) in self.boxes:
                    buffer += "O"
                    continue
                buffer += "."
            buffer += "\n"
        print(buffer)

    def follow_robot_instructions(self, instructions: str) -> Self:
        """Return new Map after following instructions."""
        # Create mutable copies
        robot = self.robot
        boxes = set(self.boxes)

        # print("Initial State:")
        for instruction in instructions:
            # self._replace(robot=robot, boxes=boxes).render_map()
            # print(f'Move {instruction}:')
            delta = INSTRUCTION_LOOKUP[instruction]
            new_robot_vec = robot + delta
            new_robot = vec2_to_int(new_robot_vec)
            if new_robot in self.walls:
                # print("robot hits wall")
                # Discard all work, move not possible
                continue
            new_boxes = boxes
            if new_robot in boxes:
                # print("robot hits box")
                # Will be mutating boxes then, make copy
                new_boxes = set(boxes)

                # Can get away with only remembering position change,
                # moving entire chain one by one is equivalent to moving
                # first box to end position
                box_destination = new_robot_vec
                while vec2_to_int(box_destination) in new_boxes:
                    box_destination += delta

                # If end of chain is in a wall, bad
                if vec2_to_int(box_destination) in self.walls:
                    # print("box chain hits wall")
                    # Discard all work, move not possible
                    continue
                # print("boxes move")
                # New robot position = box chain head original position
                new_boxes.remove(new_robot)
                new_boxes.add(vec2_to_int(box_destination))

            # Update data, move was successful
            boxes = new_boxes
            robot = new_robot_vec
            # break
        # self = self._replace(robot=robot, boxes=boxes)
        # self.render_map()
        # return self
        return self._replace(robot=robot, boxes=frozenset(boxes))

    def boxes_as_gps(self) -> Generator[int, None, None]:
        """Yield box good position system numbers."""
        for x, y in self.boxes:
            yield y * 100 + x


class DoubleMap(NamedTuple):
    """Double Map Object."""

    boxes: frozenset[tuple[tuple[int, int], tuple[int, int]]]
    walls: frozenset[tuple[int, int]]
    robot: Vector2

    @classmethod
    def read_map(cls, map_data: list[str]) -> Self:
        """Return new Map object from map data."""
        boxes: set[tuple[tuple[int, int], tuple[int, int]]] = set()
        walls: set[tuple[int, int]] = set()
        robot = Vector2(0, 0)

        for y, line in enumerate(map_data):
            last_left = (0, 0)
            for x, char in enumerate(line):
                if char == "@":
                    robot = Vector2(x, y)
                    continue
                if char == "#":
                    walls.add((x, y))
                    continue
                if char == "[":
                    last_left = (x, y)
                    continue
                if char == "]":
                    boxes.add((last_left, (x, y)))
                    continue
                if char == ".":
                    continue
                raise ValueError(char)
        return cls(
            frozenset(boxes),
            frozenset(walls),
            robot,
        )

    def render_map(self) -> None:
        """Render and print robot map to console."""
        # Find dimensions
        end_x, end_y = 0, 0
        for x, y in self.walls:
            end_x = max(end_x, x)
            end_y = max(end_y, y)

        # Type checker convinced Vector2 != tuple[int, int]
        robot = vec2_to_int(self.robot)

        # Find left and right boxes
        boxes_left = set()
        boxes_right = set()
        for left, right in self.boxes:
            boxes_left.add(left)
            boxes_right.add(right)

        # Will print out all at once for lag purposes
        buffer = ""
        for y in range(end_y + 1):
            for x in range(end_x + 1):
                if (x, y) == robot:
                    buffer += "@"
                    continue
                if (x, y) in self.walls:
                    buffer += "#"
                    continue
                if (x, y) in boxes_left:
                    buffer += "["
                    continue
                if (x, y) in boxes_right:
                    buffer += "]"
                    continue
                buffer += "."
            buffer += "\n"
        print(buffer)

    @staticmethod
    def point_hits_box(
        point: tuple[int, int],
        boxes: Collection[tuple[tuple[int, int], tuple[int, int]]],
    ) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """Return doubl box that given point hits or None."""
        for box in boxes:
            left, right = box
            if point in box:
                return box
        return None

    @staticmethod
    def move_box(
        box: tuple[tuple[int, int], tuple[int, int]],
        delta: Vector2,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return new double box after moving current one by delta."""
        left, right = box
        return (
            vec2_to_int(Vector2.from_iter(left) + delta),
            vec2_to_int(Vector2.from_iter(right) + delta),
        )

    def follow_robot_instructions(self, instructions: str) -> Self:
        """Return new Map after following instructions."""
        # Create mutable copies
        robot = self.robot
        boxes = set(self.boxes)

        # print("Initial State:")
        for instruction in instructions:
            # self._replace(robot=robot, boxes=boxes).render_map()
            # print(f'Move {instruction}:')
            delta = INSTRUCTION_LOOKUP[instruction]
            new_robot_vec = robot + delta
            new_robot = vec2_to_int(new_robot_vec)
            if new_robot in self.walls:
                # print("robot hits wall")
                # Discard all work, move not possible
                continue
            # Might not need to mutate boxes
            new_boxes = boxes

            # Potentially get double box that robot hits
            current_box = self.point_hits_box(new_robot, boxes)
            if current_box is not None:
                # print("robot hits box")
                # Ok will need to mutate
                new_boxes = set(boxes)

                to_move: set[tuple[tuple[int, int], tuple[int, int]]] = set()
                hits_wall = False
                for sub_box in current_box:
                    if sub_box in self.walls:
                        hits_wall = True
                        break

                if not hits_wall:
                    to_move.add(current_box)

                moved = []
                # While boxes to mvoe
                while to_move:
                    current_box = to_move.pop()

                    # Move box
                    moved_box = self.move_box(current_box, delta)
                    # print(f'{moved_box = }')
                    # Remember move for later
                    moved.append((current_box, moved_box))

                    # Check for wall hits and other box hits
                    for sub_box in moved_box:
                        if sub_box in self.walls:
                            hits_wall = True
                            break
                        hit_box = self.point_hits_box(sub_box, boxes)
                        if hit_box is not None and hit_box != current_box:
                            to_move.add(hit_box)
                    if hits_wall:
                        break
                if hits_wall:
                    # print("box chain hits wall")
                    # Discard all work, move not possible
                    continue
                # print("boxes move")

                # Would like to just add and remove in main at once, but
                # in some cases can be trying to remove before added or
                # something, didn't look into it much and this works.
                to_add = set()
                to_remove = set()
                for original_box, new_box in reversed(moved):
                    to_remove.add(original_box)
                    to_add.add(new_box)
                new_boxes = (new_boxes - to_remove) | to_add

            # Update boxes and robot position
            boxes = new_boxes
            robot = new_robot_vec
            # break
        # self = self._replace(robot=robot, boxes=boxes)
        # self.render_map()
        # return self
        return self._replace(robot=robot, boxes=frozenset(boxes))

    def boxes_as_gps(self) -> Generator[int, None, None]:
        """Yield box good position system numbers."""
        for (x, y), _right in self.boxes:
            yield y * 100 + x


def yield_double_map(map_data: list[str]) -> Generator[str, None, None]:
    """Yield doubled map data."""
    for line in map_data:
        for char in line:
            if char == "#":
                yield "##"
            elif char == "O":
                yield "[]"
            elif char == ".":
                yield ".."
            elif char == "@":
                yield "@."
            else:
                raise ValueError(char)
        yield "\n"


def run() -> None:
    """Run program."""
    data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    ##    data = """########
    ###..O.O.#
    ####@.O..#
    ###...O..#
    ###.#.O..#
    ###...O..#
    ###......#
    ##########
    ##
    ##<^^>>>vv<v>>v<<"""
    ##    data = """#######
    ###...#.#
    ###.....#
    ###..OO@#
    ###..O..#
    ###.....#
    #########
    ##
    ##<vv<<^^<<^^"""
    data_file = Path(__file__).absolute().parent / "day15.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    gen = iter(data.splitlines())
    map_data = []
    # Read until blank line, then it's instruction data
    for line in gen:
        if not line:
            break
        map_data.append(line)

    # Read instruction data
    instructions = ""
    for line in gen:
        instructions += line

    # Read map
    map_ = Map.read_map(map_data)
    # map_.render_map()

    # Follow instructions
    map_ = map_.follow_robot_instructions(instructions)
    print(f"{sum(map_.boxes_as_gps()) = }")

    # Double map
    double_map_data = (
        ("".join(yield_double_map(map_data))).rstrip().splitlines()
    )
    # Read map data
    double_map = DoubleMap.read_map(double_map_data)
    # double_map.render_map()

    # Follow instructions
    double_map = double_map.follow_robot_instructions(instructions)
    print(f"{sum(double_map.boxes_as_gps()) = }")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
