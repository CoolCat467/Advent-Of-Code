#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 18 - https://adventofcode.com/2021/day/19

"""Goals:
1)
2).
"""  # noqa: D205

from __future__ import annotations

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 19"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

from vector import Vector


class Cube:  # noqa: D101
    def __init__(self, center: Vector, side_len: int) -> None:
        """Initialize cube."""
        self.center = center
        self.side_len = side_len
        self.points: dict[str, Vector] = {}
        self.gen_points()

    def gen_points(self) -> None:
        "Generate points."  # noqa: D300
        half = self.side_len / 2
        self.points.clear()
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    vec = (Vector(x, y, z) * 2 - 1) * half
                    name = "".join(map(str, (x, y, z)))
                    self.points[name] = self.center + vec
                    print(f"{vec} -> {name}")

    def check_z(self, z: int) -> bool:
        "Return True if z within z bounds."  # noqa: D300
        if z < self.points["000"][2]:  # less than min z
            return False
        return z <= self.points["001"][2]  # greater than max z

    def check_y(self, y: int) -> bool:
        "Return True if y within y bounds."  # noqa: D300
        if y < self.points["000"][1]:  # less than min y
            return False
        return y <= self.points["010"][1]  # greater than max y

    def check_x(self, x: int) -> bool:
        "Return True if x within x bounds."  # noqa: D300
        if x < self.points["000"][0]:  # less than min x
            return False
        return x <= self.points["100"][0]  # greater than max x

    def check(self, point: Vector) -> bool:
        "Return True if point within cube area."  # noqa: D300
        x, y, z = point
        return self.check_x(x) and self.check_y(y) and self.check_z(z)


class Scanner:  # noqa: D101
    def __init__(self, points: list[tuple[int, ...]]) -> None:
        """Initialize scanner."""
        self.points = [Vector.from_iter(p) for p in points]

    def __repr__(self) -> str:
        """Return representation of scanner."""
        return "<Scanner>"

    def get_abs(self) -> list[Vector]:
        """Return absolute value vectors."""
        return [abs(v) for v in self.points]

    def find_matches(self, scanner: Scanner) -> list[Vector]:
        """Return matches."""
        points = scanner.get_abs()
        print(points)
        print(self.get_abs())
        matches = []
        for idx, point in enumerate(self.get_abs()):
            if point in points:
                matches.append(self.points[idx])
        return matches


def run() -> None:
    "Solve problems."  # noqa: D300
    # Read file
    ##with open("adv19.txt", encoding="utf-8") as rfile:
    ##    # types: assignment error: Incompatible types in assignment (expression has type "str", variable has type "list[Any]")
    ##    data = rfile.read()
    ##    # types: ^^^^^^^^^^
    ##    rfile.close()
    data = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
    # Process data
    scan_tables: list[str] = data.split("\n\n")
    raw_scanners = {}
    for scan_table in scan_tables:
        scan_data = scan_table.splitlines()
        name = scan_data[0]
        scan_data = scan_data[1:]
        name = (
            name.replace("---", "").replace(" scanner ", "").replace(" ", "")
        )
        raw_scanners[name] = [tuple(map(int, x.split(","))) for x in scan_data]
    ##    print(scanners)

    # Solve 1
    scanners: dict[str, Scanner] = {
        k: Scanner(v) for k, v in raw_scanners.items()
    }
    diff = scanners["0"].find_matches(scanners["1"])
    print(scanners)
    print(diff)

    # Solve 2


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
