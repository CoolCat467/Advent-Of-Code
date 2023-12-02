"""Advent of Code 2023 Day 2."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 2"
__author__ = "CoolCat467"
__version__ = "0.0.0"

from typing import Final, NamedTuple, Self, SupportsIndex


class Round(NamedTuple):
    """Represents one dice round."""

    r: int = 0
    g: int = 0
    b: int = 0

    def __add__(self, rhs: tuple[int, int, int] | object) -> Self:
        """Return component-wise addition of this round with another tuple."""
        if not isinstance(rhs, tuple) or len(rhs) != 3:
            raise ValueError("Invalid operand")
        return self.__class__(*(a + b for a, b in zip(self, rhs, strict=True)))

    def __mul__(self, rhs: SupportsIndex) -> Self:
        """Multiply each component by rhs."""
        if not isinstance(rhs, int):
            raise ValueError("Invalid operand")
        return self.__class__(*(x * rhs for x in self))

    def maximum(self, rhs: tuple[int, int, int]) -> Self:
        """Return component-wise max of this Round with another tuple."""
        return self.__class__(
            *(max(a, b) for a, b in zip(self, rhs, strict=True)),
        )


UNIT_COLORS: Final = {
    "red": Round(1, 0, 0),
    "green": Round(0, 1, 0),
    "blue": Round(0, 0, 1),
}


def parse_game(text: str) -> tuple[int, list[Round]]:
    """Parse game into tuple of game ID and list of Round objects."""
    game_id, round_info = text.removeprefix("Game ").split(": ", 1)

    rounds = []
    for round_ in round_info.split("; "):
        current_round = Round(0, 0, 0)
        for color_data in round_.split(", "):
            count, color = color_data.split(" ", 1)
            current_round += UNIT_COLORS[color] * int(count)
        rounds.append(current_round)
    return int(game_id), rounds


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    possible_one = 0
    power_sum_two = 0
    for game_text in text.splitlines():
        game_id, rounds = parse_game(game_text)
        current_max = Round(0, 0, 0)
        for round_ in rounds:
            current_max = current_max.maximum(round_)

        r, g, b = current_max
        if r <= 12 and g <= 13 and b <= 14:
            possible_one += game_id

        power = r * g * b
        power_sum_two += power

    return possible_one, power_sum_two


def run() -> None:
    """Print answer."""
    input_ = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    ##    with open("day2.txt", encoding="utf-8") as file:
    ##        input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
