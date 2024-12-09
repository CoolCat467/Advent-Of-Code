#!/usr/bin/env python3

"""Combine Results - Combine multiple program outputs into one file."""

# Programmed by CoolCat467

from __future__ import annotations

# Combine Results - Combine multiple program outputs into one file.
# Copyright (C) 2024  CoolCat467
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__title__ = "Combine Results"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


import io
import subprocess
from difflib import unified_diff
from functools import partial
from typing import TYPE_CHECKING, cast

import trio

if TYPE_CHECKING:
    from collections.abc import Sequence

type AsyncWriteBytes = trio._file_io.AsyncIOWrapper[io.BufferedWriter]
type AsyncReadBytes = trio._file_io.AsyncIOWrapper[io.BufferedReader]


# bi format specs: https://github.com/tsoding/bi-format
async def write_int_field(
    fp: AsyncWriteBytes,
    name: bytes,
    value: int,
) -> None:
    """Write integer field to file."""
    await fp.write(b":i %s %d\n" % (name, value))


async def write_blob_field(
    fp: AsyncWriteBytes,
    name: bytes,
    blob: bytes,
) -> None:
    """Write binary blob field to file."""
    await fp.write(b":b %s %d\n" % (name, len(blob)))
    await fp.write(blob)
    await fp.write(b"\n")


async def write_array_field(
    fp: AsyncWriteBytes,
    name: bytes,
    blobs: Sequence[bytes],
) -> None:
    """Write multiple binary blob fields to file."""
    await write_blob_field(fp, name, str(len(blobs)).encode("utf-8"))
    for index, blob in enumerate(blobs):
        await write_blob_field(fp, b"%s_%i" % (name, index), blob)


async def read_int_field(fp: AsyncReadBytes, name: bytes) -> int:
    """Read integer field from file."""
    line = await fp.readline()
    field = b":i " + name + b" "
    assert line.startswith(field)
    assert line.endswith(b"\n")
    return int(line[len(field) : -1])


async def read_blob_field(fp: AsyncReadBytes, name: bytes) -> bytes:
    """Read blob field from file."""
    line = await fp.readline()
    field = b":b " + name + b" "
    assert line.startswith(field), field
    assert line.endswith(b"\n")
    size = int(line[len(field) : -1])
    blob = await fp.read(size)
    assert await fp.read(1) == b"\n"
    return blob


async def read_array_field(fp: AsyncReadBytes, name: bytes) -> list[bytes]:
    """Read blob field from file."""
    item_count = int((await read_blob_field(fp, name)).decode("utf-8"))
    blobs = []
    for index in range(item_count):
        blobs.append(await read_blob_field(fp, b"%s_%i" % (name, index)))
    return blobs


async def run() -> None:
    """Run program."""
    this_file = await trio.Path(__file__).absolute()
    this_folder = this_file.parent
    # Make sure in right folder
    assert await (this_folder / "LICENSE").exists()
    script_dir = this_folder / "2024"
    assert await script_dir.exists()
    result_file = this_folder / "results.bi"

    prior_results: list[bytes] | None = None
    if await result_file.exists():
        print("Loading prior results...")
        async with await result_file.open("rb") as fp:
            prior_results = await read_array_field(fp, b"results")

    scripts = sorted(
        file for file in await script_dir.iterdir() if file.suffix == ".py"
    )
    processes = []
    async with trio.open_nursery() as nursery:
        for script in scripts:
            print(f"Starting to run {script.name!r}...")
            processes.append(
                cast(
                    trio.Process,
                    await nursery.start(
                        partial(
                            trio.run_process,
                            ("python", script),
                            stdout=subprocess.PIPE,
                        ),
                    ),
                ),
            )
        print("Waiting for all scripts to complete...")

    print("Action complete. Reading results...")
    results = []
    for index, process in enumerate(processes):
        assert process.stdout is not None
        async with process.stdout as process_fp:
            buffer = bytearray()
            async for byte in process_fp:
                buffer.extend(byte)
            if (
                prior_results
                and index < len(prior_results)
                and prior_results[index] != buffer
            ):
                # Show differences
                a = (
                    prior_results[index]
                    .decode("utf-8")
                    .splitlines(keepends=True)
                )
                b = buffer.decode("utf-8").splitlines(keepends=True)
                print(f"UNEXPECTED: {scripts[index].name} changed")
                print(
                    "".join(
                        unified_diff(
                            a,
                            b,
                            fromfile="expected",
                            tofile="actual",
                        ),
                    ),
                )
            results.append(buffer)

    print("Saving results, please do not turn off the power...")
    async with await result_file.open("wb") as fp:
        await write_array_field(
            fp,
            b"results",
            results,
        )
    print("Save complete.")


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    trio.run(run)
