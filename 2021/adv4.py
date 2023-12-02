#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 4 - https://adventofcode.com/2021/day/4

"""Goals:
1) Find board that will win bingo against the giant squid first
2) Find board that will be last to win bingo against giant squid so we don't
make it mad at us.
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 4"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from collections import deque

import numpy as np


class BingoBoard:
    "Bingo board object."  # noqa: D300
    dim = (5, 5)
    has = "X"

    def __init__(self, values):  # noqa: D107
        self.board = np.array(values, dtype=str).reshape(self.dim)
        self.original = np.array(values, dtype=int).reshape(self.dim)
        self.to_win = []
        self.won_prev = False

    def __repr__(self):  # noqa: D105
        return str(self.board)

    def has_won(self):
        "Return True if this board has won."  # noqa: D300
        rows, cols = self.board.shape
        for row in self.board[:]:
            if "".join(row) == self.has * rows:
                return True
        for column in range(cols):
            col = self.board[:, column]
            if "".join(col) == self.has * cols:
                return True
        return False

    def drew(self, value):
        "Draw value, update data, and return bool of if won this round."  # noqa: D300
        new = self.board.flatten().copy()
        for idx, cval in enumerate(new):
            if cval == str(value):
                new[idx] = self.has
        self.board = new.reshape(self.dim)
        if not self.won_prev:
            self.to_win.append(value)
            self.won_prev = self.has_won()
            return self.won_prev
        return False

    def get_marked_unmarked(self):
        "Return dictionary, key is bool of if values were part of win."  # noqa: D300
        yesno = {0: [], 1: []}
        for value in self.original.flatten():
            yesno[value in self.to_win].append(value)
        return yesno

    def get_score(self):
        "Get the score of this board. 0 if not won."  # noqa: D300
        if not self.won_prev:
            return 0
        in_not = self.get_marked_unmarked()
        unmarked = in_not[0]
        return sum(unmarked) * self.to_win[-1]


class BoardControler:
    "Board controller."  # noqa: D300

    def __init__(self, order, boards):  # noqa: D107
        self.order = deque(order)
        self.boards = boards

    @classmethod
    def read_file(cls, data):
        "Read data from file and return new class instance."  # noqa: D300
        lines = data.splitlines()

        order = list(map(int, lines[0].split(",")))

        boards = []

        value = []
        for line in lines[2:]:
            if " " in line:
                for item in line.split(" "):
                    if item:
                        value.append(item)
                continue
            boards.append(BingoBoard(value))
            value = []
        return cls(order, boards)

    def check_won(self):
        "Return list of boards that have won now or previously."  # noqa: D300
        won = []
        for idx, board in enumerate(self.boards):
            if board.won_prev:
                won.append(idx)
        return won

    def total_won(self):
        "Return the number of boards that have won now or previously."  # noqa: D300
        return len(self.check_won())

    def waiting_count(self):
        "Return the number of boards we are waiting for to win."  # noqa: D300
        return len(self.boards) - self.total_won()

    def still_waiting(self):
        "Return True if still waiting for a board to win."  # noqa: D300
        return self.waiting_count() > 0

    def draw(self):
        "Draw a number, update boards, and return ones that win now."  # noqa: D300
        value = self.order.popleft()
        won = []
        for idx, board in enumerate(self.boards):
            if board.drew(value):
                won.append(idx)
        return won

    def get_scores(self):
        "Return score for each board as dictionary."  # noqa: D300
        scores = {}
        for idx, board in enumerate(self.boards):
            scores[idx] = board.get_score()
        return scores


def combine_and(data: list) -> str:
    "Join values of text, and have 'and' with the last one properly."  # noqa: D300
    data = list(data)
    if len(data) >= 2:
        data[-1] = "and " + data[-1]
    if len(data) > 2:
        return ", ".join(data)
    return " ".join(data)


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv4.txt", encoding="utf-8") as rfile:
        data = rfile.read()
        rfile.close()
    # Solve 1
    controller = BoardControler.read_file(data)
    won = False
    has1 = False
    while controller.still_waiting():
        won = controller.draw()
        if won:
            scores = controller.get_scores()
            if not has1:
                print(scores[won[0]])
                has1 = True
    # Solve 2
    print(scores[won[0]])


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
