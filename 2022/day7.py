#!/usr/bin/env python3  # noqa: EXE001
# Advent of Code 2022 Day 7

"Advent of Code 2022 Day 7."  # noqa: D300

# Programmed by CoolCat467
from __future__ import annotations

__title__ = "Advent of Code 2022 Day 7"
__author__ = "CoolCat467"
__version__ = "0.0.0"

import io
from typing import Any


def create_fs_map(lines: list[str]) -> dict[str, Any]:
    "Get file map from lines."  # noqa: D300
    dirs: dict[str, Any] = {}

    follow = [""]
    last_command = ""
    for line in lines:
        if line.startswith("$"):
            match line[2:].split(" "):
                case ("ls",):
                    last_command = "ls"
                case ("cd", path):
                    if path == "..":
                        follow.pop()
                    elif path == "/":
                        follow.clear()
                        follow.append("")
                    else:
                        follow.append(path)
                    last_command = "cd"
                case _:
                    print("error")
        elif last_command == "cd":
            print(f"error: {last_command = }, did not expect output")
        elif last_command != "ls":
            print(f"error: {last_command = }, unexpected command")
        elif line.startswith("dir"):
            continue
        else:
            size_str, filename = line.split(" ", 1)
            file = (filename, int(size_str))
            if follow[0] not in dirs:
                dirs[follow[0]] = {}
            part = dirs[follow[0]]
            for link in follow[1:]:
                if link not in part:
                    part[link] = {}
                part = part[link]
            if "" not in part:
                part[""] = [file]
            else:
                part[""].append(file)
    return dirs


def dir_usage(lines: list[str]) -> tuple[int, dict[tuple[str, ...], int]]:
    "Read the lines and get the directory sums."  # noqa: D300
    files = create_fs_map(lines)

    def read_dict(cdict: dict[str, Any]) -> dict[tuple[str, ...], int]:
        "Read a dictionary and return paths."  # noqa: D300
        sizes: dict[tuple[str, ...], int] = {}
        for path in cdict:
            nxt = cdict[path]
            # See next object.
            if isinstance(nxt, dict):
                # If dictionary, read and add our own path.
                add = read_dict(nxt)
                for file, size in add.items():
                    save: tuple[str, ...]
                    save = (path,) if file == ("",) else (path, *file)
                    for segment in range(1, len(save) + 1):
                        part = save[:segment]
                        if part not in sizes:
                            sizes[part] = 0
                    sizes[save] += size
            else:
                # If it's a list or tuple, add all to our own paths joined.
                for _, size in nxt:
                    if (path,) not in sizes:
                        sizes[(path,)] = 0
                    sizes[(path,)] += size
        return sizes

    dir_sums = read_dict(files)
    file_sum = sum(dir_sums.values())

    handled: set[tuple[str, ...]] = set()
    all_folders = set(dir_sums)

    while folders := tuple(all_folders - handled):
        idx = 0
        for nidx, folder in enumerate(folders):
            if len(folder) > len(folders[idx]):
                idx = nidx
        part = folders[idx][:-1]
        if part:
            dir_sums[part] += dir_sums[folders[idx]]
        handled.add(folders[idx])
    return file_sum, dir_sums


def part_one(dir_sums: dict[tuple[str, ...], int]) -> int:
    "Find sum of directories with a total size of at most 100000."  # noqa: D300
    return sum(folder for folder in dir_sums.values() if folder <= 100000)


def part_two(file_sum: int, dir_sums: dict[tuple[str, ...], int]) -> int:
    "Find the total size of smallest directory to delete to allow software update."  # noqa: D300
    total_available = 70000000
    required_unused = 30000000
    ##    print(f'{file_sum = }')

    unused_map: list[int] = []
    for _, usage in dir_sums.items():
        removed = file_sum - usage
        if required_unused + removed <= total_available:
            unused_map.append(usage)
    ##    print(list(sorted(unused_map)))
    return min(unused_map)


def run() -> None:
    "Synchronous entry point."  # noqa: D300, D401
    test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    file = io.StringIO(test_data)
    ##    file = open('day7.txt', encoding='utf-8')

    lines = file.read().splitlines()
    file.close()

    file_sum, dir_sums = dir_usage(lines)

    print(f"{part_one(dir_sums)           = }")
    print(f"{part_two(file_sum, dir_sums) = }")


if __name__ == "__main__":
    print(f"{__title__}\nProgrammed by {__author__}.\n")
    run()
