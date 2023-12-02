#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 2

"Advent of Code 2022 Day 2."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 2"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import io


def get_win(opponent: int, us: int) -> int:
    "Get if won against opponent given opponent action and our action."  # noqa: D300
    if opponent == us:
        return 3
    if (opponent + 1) % 3 == us:
        return 6
    return 0


def score_strategy_incorrectly(strategy: list[tuple[str, str]]) -> int:
    "Score strategy if is list of opponent action and our action."  # noqa: D300
    score = 0
    for given, do in strategy:
        opponent = ord(given) - 65
        us = ord(do) - 88
        score += us + 1
        win = get_win(opponent, us)
        score += win
    return score


def get_action(opponent: int, win: int) -> int:
    "Get action go get game to win state given opponent action."  # noqa: D300
    if win == 3:
        return opponent
    if win == 0:
        us = opponent - 1
        if us < 0:
            return 2
        return us
    return (opponent + 1) % 3


def score_strategy_correctly(strategy: list[tuple[str, str]]) -> int:
    "Score strategy if is list of opponent action and required game state."  # noqa: D300
    score = 0
    for given, result in strategy:
        opponent = ord(given) - 65
        win = (ord(result) - 88) * 3
        score += win
        score += get_action(opponent, win) + 1
    return score


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """A Y
B X
C Z"""
    file = io.StringIO(test_data)
    ##    file = open('day2.txt', encoding='utf-8')
    strategy: list[tuple[str, str]] = []
    for line in file:
        given, do = line.strip().split(" ")
        strategy.append((given, do))
    file.close()
    print(score_strategy_incorrectly(strategy))
    print(score_strategy_correctly(strategy))


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
