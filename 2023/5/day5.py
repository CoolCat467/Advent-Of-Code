"""Advent of Code 2023 Day 5."""

# Programmed by CoolCat467

from __future__ import annotations

__title__ = "2023 Day 5"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import itertools
from typing import NamedTuple, Self

assert hasattr(itertools, "batched"), "Requires Python 3.12+"


class DataOne(NamedTuple):
    """Data for part 1."""

    category: str
    values: tuple[int, ...]

    @classmethod
    def from_seeds(cls, seed_data: str) -> Self:
        """Return data from seeds entry."""
        return cls(
            "seed",
            tuple(map(int, seed_data.removeprefix("seeds: ").split(" "))),
        )


class DataTwo(NamedTuple):
    """Data for part 2."""

    category: str
    values: tuple[tuple[int, int], ...]

    @classmethod
    def from_seeds(cls, seed_data: str) -> Self:
        """Return data from seeds entry."""
        itertools.batched(
            map(int, seed_data.removeprefix("seeds: ").split(" ")),
            2,
        )
        return cls(
            "seed",
            tuple(
                itertools.batched(
                    map(int, seed_data.removeprefix("seeds: ").split(" ")),
                    2,
                ),
            ),
        )


def ranges_overlap(x1: int, x2: int, y1: int, y2: int) -> bool:
    """Return if range [x1, x2] overlaps with range [y1, y2]."""
    assert x1 <= x2
    assert y1 <= y2
    return x1 <= y2 and y1 <= x2


class Category(NamedTuple):
    """Almenac Category."""

    source_type: str
    destination_type: str
    range_maps: tuple[tuple[tuple[int, int], tuple[int, int]], ...]

    @classmethod
    def from_string(cls, category_string: str) -> Self:
        """Return category from category entry."""
        map_header, *range_data = category_string.splitlines()
        source_type, destination_type = map_header.removesuffix(" map:").split(
            "-to-",
        )

        range_maps = []
        for range_entry in range_data:
            dest_range_start, src_range_start, length = map(
                int,
                range_entry.split(" "),
            )
            ##            src = (src_range_start, src_range_start+length)
            ##            dest = (dest_range_start, dest_range_start+length)
            ##            range_maps.append((src, dest))
            range_maps.append((dest_range_start, src_range_start, length))
        return cls(source_type, destination_type, tuple(range_maps))

    def apply_mapping_one(self, data: DataOne) -> DataOne:
        """Return new data after applying mapping (part one)."""
        assert data.category == self.source_type

        results = []
        for item in data.values:
            handled = False
            for dest_start, src_start, range_length in self.range_maps:
                ##                src_start, src_end = src
                if item not in range(src_start, src_start + range_length):
                    continue
                ##                dest_start, _dest_end = dest

                start_offset = item - src_start
                results.append(dest_start + start_offset)
                handled = True
                break
            if not handled:
                results.append(item)

        return DataOne(self.destination_type, results)

    def apply_mapping_two(self, data: DataTwo) -> DataTwo:
        """Return new data after mapping (part two)."""
        assert data.category == self.source_type

        results = []
        items = list(data.values)
        while items:
            item_start, item_length = items.pop(0)
            item_end = item_start + item_length

            handled = False
            for dest_start, src_start, range_length in self.range_maps:
                src_end = src_start + range_length
                offset = dest_start - src_start

                # No intersection
                # Item: ###    OR    ###
                # Src :    ### OR ###
                if item_end < src_start or item_start > src_end:
                    continue

                # Item: ####
                # Src :   ####
                if item_start < src_start and item_end <= src_end:
                    left = (item_start, src_start - item_start)
                    right = (left[1] + offset, item_end)
                    results.append(right)
                    items.append(left)

                # Item:   ####
                # Src : ####
                elif item_start > src_start and src_end <= item_end:
                    left = (item_start + offset, src_end - item_start)
                    right = (src_end, item_end - src_end)
                    results.append(left)
                    items.append(right)

                # Item:   ####
                # Src : ########
                elif item_start > src_start and item_end < src_end:
                    results.append((item_start + offset, item_length))

                # Item: ########
                # Src :   ####
                elif item_start < src_start and item_end > src_end:
                    left = (item_start, src_start - item_start)
                    results.append((item_start + offset, item_length))
                    right = (src_end, item_end - src_end)
                    items.append(left)
                    items.append(right)

                handled = True
                break
            if not handled:  # and item_length > 0:
                results.append((item_start, item_length))

        return DataTwo(self.destination_type, results)


def process(text: str) -> tuple[int, int]:
    """Return solutions to part one and part two given input text."""
    seed_data, *category_data = text.split("\n\n")
    seeds_one = DataOne.from_seeds(seed_data)
    # print(f'{seeds_one = }')
    DataTwo.from_seeds(seed_data)
    ##    print(f"{seeds_two = }")

    # categories: dict[str, Category] = {}
    current_one = seeds_one
    for category_string in category_data:
        ##        for start, length in current_two.values:
        ##            print(list(range(start, start+length)))
        category = Category.from_string(category_string)
        # categories[category.source_type] = category
        current_one = category.apply_mapping_one(current_one)
    ##        current_two = category.apply_mapping_two(current_two)
    ##        print(current_one)
    ##        print(current_two)
    ##    for start, length in current_two.values:
    ##        print(list(range(start, start+length)))
    ##    print(f'{categories = }')
    ##    two = min(start for start, _ in current_two.values)

    return min(current_one.values), 0


def run() -> None:
    """Print answer."""
    input_ = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    ##    with open("day5.txt", encoding="utf-8") as file:
    ##        input_ = file.read()
    print("Part 2 currently broken.")
    print(f"{process(input_) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
