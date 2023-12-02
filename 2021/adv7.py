#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 7 - https://adventofcode.com/2021/day/7

"""Goals:
1) Align crab submarines with lowest fuel, fuel is move distance.
2) Align crab submarines with lowest fuel, but fuel for 1 space is last space + 1,
so sum of range(distance), which is apparently distance*(distance-1)/2.
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 7"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0


# pylint: disable=R0903
class Align:
    "Align points using fuel_move to score fuel consumption."  # noqa: D300

    def __init__(self, points, fuel_move):  # noqa: D107
        self.points = points
        self.fuel_move = fuel_move

    def min_align(self):
        "Return alignment with least fuel usage."  # noqa: D300
        alignments = {}
        for align in range(max(self.points)):
            fuel = 0
            for point in self.points:
                fuel += self.fuel_move(point, align)
            if align not in alignments:
                alignments[fuel] = []
            alignments[fuel].append(align)
        return min(alignments)


def run():
    "Solve problems."  # noqa: D300
    # read file
    data = []
    with open("adv7.txt", encoding="utf-8") as rfile:
        data = rfile.read().split(",")
        rfile.close()
    ##    data = """16,1,2,0,4,2,7,1,2,14""".split(',')
    data = list(map(int, data))
    # Solve 1
    align = Align(data, lambda p, align: abs(align - p))
    print(align.min_align())

    # Solve 2
    def score_fuel(current, target):
        dist = abs(current - target)
        ##        return sum(range(1, dist+1))
        # https://stackoverflow.com/a/43529010
        return int(dist * (dist + 1) / 2)
        # return = ((end*(end+1))//2 - ((start-1)*(start))//2)*5 + (end-start+1)*17

    align = Align(data, score_fuel)
    print(align.min_align())


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
