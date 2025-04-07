#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 10 - https://adventofcode.com/2021/day/10

"""Goals:
1) What is the total syntax error score for those errors?
2) What is the middle score for auto-completion?.
"""  # noqa: D205

# Programmed by CoolCat467

from collections import deque

__title__ = "Advent of Code 2021 - Day 10"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

OPENS = ("(", "[", "{", "<")
CLOSES = (")", "]", "}", ">")
ERROR_SCORES = (3, 57, 1197, 25137)
AUTO_SCORES = (1, 2, 3, 4)


def parse_line(line):
    "Parse line and return."  # noqa: D300
    errors = dict.fromkeys(range(len(CLOSES)), 0)
    stack = deque()
    for char in line:
        if char not in OPENS and char not in CLOSES:
            print(f"Invalid character: {char}")
            continue
        if char in OPENS:
            stack.append(OPENS.index(char))
        elif char in CLOSES:
            started = stack.pop()
            index = CLOSES.index(char)
            if index != started:
                errors[index] += 1
    auto_score = 0
    add = ""
    while stack:
        auto_score *= 5
        value = stack.pop()
        auto_score += AUTO_SCORES[value]
        add += CLOSES[value]
    error_score = sum(
        count * mult
        for count, mult in zip(errors.values(), ERROR_SCORES, strict=False)
    )
    return error_score, auto_score


def parse_lines(lines):
    "Parse lines and return error and autocomplete scores."  # noqa: D300
    error_score = 0
    auto_scores = []
    for line in lines:
        result = parse_line(line)
        error_score += result[0]
        if not result[0]:
            auto_scores.append(result[1])
    auto_scores = sorted(auto_scores)
    middle = (len(auto_scores) + 1) // 2 - 1
    auto_score = auto_scores[int(middle)]
    return error_score, auto_score


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv10.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    ##    data = """[({(<(())[]>[[{[]{<()<>>
    ##[(()[<>])]({[<{<<[]>>(
    ##{([(<{}[<>[]}>{[]{[(<()>
    ##(((({<>}<{<{<>}{[]{[]{}
    ##[[<[([]))<([[{}[[()]]]
    ##[{[{({}]{}}([{[{{{}}([]
    ##{<[[]]>}<{[{[{[]{()[[[]
    ##[<(<(<(<{}))><([]([]()
    ##<{([([[(<>()){}]>(<<{{
    ##<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()
    # Solve 1
    result = parse_lines(data)
    print(result[0])
    # Solve 2
    print(result[1])


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
