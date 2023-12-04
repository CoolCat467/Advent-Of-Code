"""Advent of Code 2023 Day 4."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 4"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import re
from typing import Final, Generator

NUMBER_REGEX: Final = re.compile(r"\d+")


def find_numbers(line: str) -> Generator[int, None, None]:
    """Yield number matches in given line."""
    for match in NUMBER_REGEX.finditer(line):
        yield int(match.group(0))


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    points = 0
    card_values: dict[int, int] = {}
    card_wins: dict[int, int] = {}
    for line in text.splitlines():
        # Parse important data from line
        card, data = line.split(": ", 1)
        card_id = int(card.removeprefix("Card ").strip())
        winning, have = data.split(" | ")

        # Test shows that winning numbers and numbers we have are unique
        win_numbers = set(find_numbers(winning))
        have_numbers = set(find_numbers(have))

        # This works well because we can get a set of when they have matches
        have_wins = have_numbers & win_numbers
        match_count = len(have_wins)

        # Part one
        if match_count:
            points += 1 << (match_count - 1)
        # Part two
        card_wins[card_id] = 1
        card_values[card_id] = match_count

    # Handle card wins
    total_cards = 0
    while card_wins:
        # Pop smallest
        card_id = min(card_wins)
        win_count = card_wins.pop(card_id)
        # print(f'{card_id}: {win_count}')

        # Add to total
        total_cards += win_count

        # Get number of cards we win from this card
        after_count = card_values[card_id]
        for after in range(after_count):
            # ID of next card
            new_card = after + card_id + 1  # +1 is very important!
            if new_card not in card_values:
                # Ignore invalid
                break
            # Add wins for new cards
            card_wins[new_card] = card_wins.get(new_card, 0) + win_count
        # print(f'{card_wins = }')
    return points, total_cards


def run() -> None:
    """Print answer."""
    input_ = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    ##with open("day4.txt", encoding="utf-8") as file:
    ##    input_ = file.read()
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
