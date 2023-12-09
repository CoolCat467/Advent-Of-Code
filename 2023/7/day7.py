"""Advent of Code 2023 Day 7."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 7"
__author__ = "CoolCat467"
__version__ = "0.0.0"

from collections import Counter
from typing import NamedTuple


def card_value_one(card: str) -> int:
    """Return value of card (Part one)."""
    try:
        return int(card)
    except ValueError:
        return ("T", "J", "Q", "K", "A").index(card) + 10


def card_value_two(card: str) -> int:
    """Return value of card (Part two)."""
    if card == "J":
        return 1
    try:
        return int(card)
    except ValueError:
        return ("T", "Q", "K", "A").index(card) + 10


def hand_type_one(hand: str) -> tuple[str, int]:
    """Return name and hand type number of given hand of cards (Part one)."""
    counter = Counter(hand)
    rev_count = {}
    for key, value in counter.items():
        rev_count[value] = rev_count.get(value, [])
        rev_count[value].append(key)
    ##    print(f'{counter = }')
    if rev_count.get(5):
        return "five-of-a-kind", 6
    if rev_count.get(4):
        return "four-of-a-kind", 5
    if rev_count.get(3) and rev_count.get(2):
        return "full-house", 4
    if rev_count.get(3):
        return "three-of-a-kind", 3
    if twos := rev_count.get(2):
        if len(twos) == 2:
            return "two-pair", 2
        return "one-pair", 1
    assert len(rev_count.get(1)) == 5
    return "high-card", 0


def hand_type_two(hand: str) -> tuple[str, int]:
    """Return name and hand type number of given hand of cards (Part two)."""
    counter = Counter(hand)
    ##    rev_count = {}
    ##    for key, value in counter.items():
    ##        rev_count[value] = rev_count.get(value, [])
    ##        rev_count[value].append(key)
    ##    print(f'{counter = }')
    ##    by_size = sorted(counter, key=lambda x: counter[x], reverse=True)
    for _type, count in counter.most_common():
        diff = 5 - count
        if counter["J"] >= diff:
            return "five-of-a-kind", 6
    for _type, count in counter.most_common():
        diff = 4 - count
        if counter["J"] >= diff:
            return "four-of-a-kind", 5
    not_has_three = True
    cur_j = counter["J"]
    for _type, count in counter.most_common():
        if not_has_three:
            if count > 3:
                continue
            # count <= 3
            diff = 3 - count
            if cur_j < diff:
                continue
            cur_j -= diff
            not_has_three = False
        else:
            if count > 2:
                continue
            # count <= 2
            diff = 2 - count
            if cur_j < diff:
                continue
            return "full-house", 4
    for type_, count in counter.most_common():
        if type_ == "J":
            continue
        count = counter[type_]
        diff = 3 - count
        if counter["J"] >= diff:
            return "three-of-a-kind", 3
    two_count = 0
    cur_j = counter["J"]
    for _type, count in counter.most_common():
        if count > 2:
            continue
        # count <= 2
        diff = 2 - count
        if cur_j < diff:
            continue
        cur_j -= diff
        two_count += 1
    if two_count == 2:
        return "two-pair", 2
    if two_count == 1:
        return "one-pair", 1
    assert len(counter) == 5
    return "high-card", 0


def parse_game(text: str) -> tuple[str, int]:
    """Parse game into tuple of game ID and list of Round objects."""
    cards, bid = text.split(" ", 1)

    return cards, int(bid)


class Hand(NamedTuple):
    """Represents a hand of cards."""

    cards: tuple[int, ...]
    type_: int
    bid: int

    def __lt__(self, right: Hand) -> bool:
        """Return if this hand is valued less than right hand (used for sorting hands)."""
        if self.type_ < right.type_:
            return True
        if self.type_ > right.type_:
            return False
        return self.cards < right.cards


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    ##    types: dict[int, list[str]] = {}
    items_one: list[Hand] = []
    items_two: list[Hand] = []
    for game_texts in text.splitlines():
        cards, bid = parse_game(game_texts)
        _name, type_one = hand_type_one(cards)
        _name_two, type_two = hand_type_two(cards)
        ##        print(f'{_name_two = }')

        items_one.append(
            Hand(tuple(card_value_one(x) for x in cards), type_one, bid),
        )
        items_two.append(
            Hand(tuple(card_value_two(x) for x in cards), type_two, bid),
        )
    ##    print(f'{items = }')

    ##    def key(left: Hand, right: Hand) -> bool:

    winnings = 0
    for index, hand in enumerate(sorted(items_one)):
        rank = index + 1
        winnings += rank * hand.bid

    winnings_two = 0
    for index, hand in enumerate(sorted(items_two)):
        ##        print(hand)
        rank = index + 1
        winnings_two += rank * hand.bid

    return winnings, winnings_two


def run() -> None:
    """Print answer."""
    input_ = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    with open("day7.txt", encoding="utf-8") as file:
        input_ = file.read()
    print("Part two is broken!")
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
