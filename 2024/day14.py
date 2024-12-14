"""Advent of Code 2024 Day 14."""

# Programmed by CoolCat467

from __future__ import annotations

# Advent of Code 2024 Day 14
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

__title__ = "Advent of Code 2024 Day 14"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Final, NamedTuple, Self

import pygame
from pygame.locals import (
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)
from pygame.time import Clock
from vector import Vector2

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

BLOCK_LOOKUP: Final = {
    3: "░",
    2: "▒",
    1: "▓",
}


def read_vec2(pos: str) -> Vector2:
    """Return Vector2 from comma-seperated numbers."""
    return Vector2.from_iter(map(int, pos.split(",", 1)))


def read_assign(assign: str) -> Vector2:
    """Return Vector2 from assignment statement."""
    return read_vec2(assign.split("=", 1)[1])


class Robot(NamedTuple):
    """Robot Object."""

    pos: Vector2
    vel: Vector2

    def multi_tick(self, ticks: int, width: int, height: int) -> Self:
        """Return new robot data after given number of ticks have happened."""
        nx, ny = self.pos + self.vel * ticks
        if nx < 0:
            nx += width
        nx %= width
        if ny < 0:
            ny += height
        ny %= height
        return self._replace(pos=Vector2(nx, ny))

    def tick(self, width: int, height: int) -> Self:
        """Return new robot data after one tick has happened."""
        return self.multi_tick(1, width, height)


def is_out_of_bounds(x: int, y: int, sx: int, sy: int, w: int, h: int) -> bool:
    """Return if given position is out of bounds."""
    return (x < sx or x >= w) or (y < sy or y >= h)


def point_in_region(x: int, y: int, sx: int, sy: int, w: int, h: int) -> bool:
    """Return if given position is within region."""
    return not is_out_of_bounds(x, y, sx, sy, w, h)


def get_counts_in_quadrents(
    robots: list[Robot],
    width: int,
    height: int,
) -> Generator[int, None, None]:
    """Yield counts of robots in quadrents."""
    mid_x = width // 2
    mid_y = height // 2
    for y in range(2):
        sy, ey = (y * mid_y + y, y * mid_y + y + mid_y)
        for x in range(2):
            sx, ex = (x * mid_x + x, x * mid_x + x + mid_x)
            count = 0
            for robot in robots:
                rx, ry = robot.pos
                if point_in_region(int(rx), int(ry), sx, sy, ex, ey):
                    count += 1
            yield count


def render_map(robots: Iterable[Robot], width: int, height: int) -> None:
    """Render and print robot map to console."""
    buffer = ""
    points = Counter((int(robot.pos.x), int(robot.pos.y)) for robot in robots)
    for y in range(height):
        for x in range(width):
            count = points[(x, y)]
            if count:
                buffer += BLOCK_LOOKUP.get(count, "█")  # str(count)
            else:
                buffer += " "  # "."
        ##print(buffer)
        ##buffer = ""
        buffer += "\n"
    print(buffer)


def render_image(
    robots: Iterable[Robot],
    width: int,
    height: int,
) -> pygame.Surface:
    """Rennder image from robots and room dimensions."""
    surface = pygame.Surface((width, height))
    points = {robot.pos for robot in robots}
    surface.lock()
    for x, y in points:
        surface.set_at((int(x), int(y)), pygame.Color(255, 255, 255))
    surface.unlock()
    # Scale up 4x
    return pygame.transform.scale2x(pygame.transform.scale2x(surface))


def part_two(base_robots: tuple[Robot, ...], width: int, height: int) -> None:
    """Handle running pygame for part two."""
    ticks = 0
    known_end = 6446

    screen = pygame.display.set_mode((width * 4, height * 4), 0, 16)
    pygame.display.set_caption(
        f"{__title__} v{__version__} [waiting for space key]",
    )
    screen.fill((0x00, 0x00, 0x00))

    clock = Clock()

    try:
        prev = -1
        running = True
        space_pressed = True  # False
        # Added after the fact to make solving animation
        ready = False
        while running and not ready:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                elif event.type == KEYUP and event.key == K_SPACE:
                    ready = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
                # Read space status
                elif event.type == KEYUP and event.key == K_SPACE:
                    space_pressed = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    space_pressed = True
                # If left or right, change by single frames
                elif event.type == KEYUP and event.key == K_LEFT:
                    ticks -= 1
                elif event.type == KEYUP and event.key == K_RIGHT:
                    ticks += 1
            # Go to next frame if space pressed
            if space_pressed:
                ticks += 1
            # Added after the fact, stop continuing if at the end
            if ticks == known_end:
                space_pressed = False
            # Re-render if outdated tick number
            if prev != ticks:
                prev = ticks
                pygame.display.set_caption(
                    f"{__title__} v{__version__} [{ticks}]",
                )

                surface = render_image(
                    (
                        robot.multi_tick(ticks, width, height)
                        for robot in base_robots
                    ),
                    width,
                    height,
                )
                screen.blit(surface, (0, 0))
                pygame.display.update()
                screen.fill((0x00, 0x00, 0x00))

            # Wait a small delay
            # Originally 10 FPS, changed to 60 FPS for animation
            clock.tick(60)  # 10)
    finally:
        print(f"{ticks = }")


def run() -> None:
    """Run program."""
    data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    ##    data = """p=2,4 v=2,-3"""
    data_file = Path(__file__).absolute().parent / "day14.txt"
    if data_file.exists():
        data = data_file.read_text().rstrip()

    robots: list[Robot] = []
    for line in data.splitlines():
        pos_str, vec_str = line.split(" ", 1)
        robots.append(Robot(read_assign(pos_str), read_assign(vec_str)))
    base_robots = tuple(robots)

    width = int(max(robot.pos.x for robot in base_robots)) + 1
    height = int(max(robot.pos.y for robot in base_robots)) + 1
    # width, height = 11, 7
    print(f"{width = } {height = }")

    post = [robot.multi_tick(100, width, height) for robot in base_robots]

    total = 1
    for count in get_counts_in_quadrents(post, width, height):
        print(f"quadrent {count = }")
        total *= count
    print(f"{total = }")

    render_map(
        (robot.multi_tick(6446, width, height) for robot in robots),
        width,
        height,
    )

    part_two(base_robots, width, height)


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    try:
        pygame.init()
        run()
    finally:
        pygame.quit()
