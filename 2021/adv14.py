#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 14 - https://adventofcode.com/2021/day/14

"""Goals:
1) What do you get if you take the quantity of the most common element and subtract the quantity
of the least common element?
2) Same as 1 but instead of 10 iterations, 40, which exponential growth makes
harder.
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 14"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

import itertools
from collections import Counter


def get_pairs(template):
    "Return pairs in template."  # noqa: D300
    return tuple(x + y for x, y in itertools.pairwise(template, template[1:]))


def insert_pairs(template, rules):
    "Insert pairs in template polymer following rules."  # noqa: D300
    data = []
    for pair in get_pairs(template):
        data.append(pair[0])
        if pair in rules:
            data.append(rules[pair])
    data.append(template[-1])
    return "".join(data)


def preform_steps(step_count, template, rules):
    "Perform step_count steps of adding stuff to template polymer following rules."  # noqa: D300
    poly = template
    for _ in range(step_count):
        poly = insert_pairs(poly, rules)
    return poly


def insert_pairs_counts(template, rules, types):
    "Insert pairs in template polymer following rules."  # noqa: D300
    for pair, count in tuple(template.items()):
        if pair not in rules or count == 0:
            continue
        new = rules[pair]
        types[new] += count
        pos = pair[0] + new, new + pair[1]
        for new_pair in pos:
            template[new_pair] += count
        template[pair] -= count
    return template, types


def preform_steps_counts(step_count, template, rules):
    "Perform step_count steps of adding stuff to template polymer following rules."  # noqa: D300
    types = Counter(template)
    poly = Counter(get_pairs(template))
    for _ in range(step_count):
        poly, types = insert_pairs_counts(poly, rules, types)
    return poly, types


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv14.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
    ##    data = """NNCB
    ##
    ##CH -> B
    ##HH -> N
    ##CB -> H
    ##NH -> C
    ##HB -> C
    ##HC -> B
    ##HN -> C
    ##NN -> C
    ##BH -> H
    ##NC -> B
    ##NB -> B
    ##BN -> B
    ##BB -> N
    ##BC -> B
    ##CC -> N
    ##CN -> C""".splitlines()
    # Format data
    template = data[0]
    pair_insert_rules = {}
    for item in data[2:]:
        key, value = item.split(" -> ")
        pair_insert_rules[key] = value
    # Solve 1
    ##    data = preform_steps(10, template, pair_insert_rules)
    ##    count = Counter(data)
    ##    values = sorted(tuple(count.values()))
    _, types = preform_steps_counts(10, template, pair_insert_rules)
    values = sorted(types.values())

    print(values[-1] - values[0])
    # Solve 2
    _, types = preform_steps_counts(40, template, pair_insert_rules)

    values = sorted(types.values())
    print(values[-1] - values[0])


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
