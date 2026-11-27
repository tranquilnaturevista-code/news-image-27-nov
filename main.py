#!/usr/bin/env python3
"""Hand the finished front page to the competition runner.

The page is painted beforehand and stored in this repository as
``entry.png``. This program is the entrypoint the runner executes: it
reads that file, confirms it is a whole PNG inside the competition's
size limits, and writes the same bytes to ``/output/entry.png`` — or to
``MAKEFUN_OUTPUT_DIR`` when the runner points elsewhere.

Only the standard library is used and the program never touches the
network, so the judge receives exactly the page stored here.
"""

import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
FALLBACK_DIR = Path("/output")

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_END = b"\x00\x00\x00\x00IEND\xaeB`\x82"


class BadEntry(Exception):
    """The stored page fails one of the competition's limits."""


def fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_header(blob):
    """Return the (width, height) of a PNG blob, or raise BadEntry."""
    if len(blob) > MAX_BYTES:
        raise BadEntry(
            f"entry.png is {len(blob)} bytes, over the 1 MiB limit")
    if not blob.startswith(PNG_MAGIC):
        raise BadEntry("entry.png does not start with a PNG signature")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        raise BadEntry("entry.png has no IHDR chunk")
    (length,) = struct.unpack(">I", blob[8:12])
    if length != 13:
        raise BadEntry("entry.png has a malformed IHDR chunk")
    width, height = struct.unpack(">II", blob[16:24])
    if width == 0 or height == 0:
        raise BadEntry("entry.png has a zero side")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise BadEntry(
            f"entry.png is {width}x{height}, over the 1024x1024 limit")
    if not blob.endswith(PNG_END):
        raise BadEntry("entry.png has no proper IEND chunk")
    return width, height


def deliver():
    if not SOURCE.is_file():
        fail("entry.png is missing next to main.py")
    blob = SOURCE.read_bytes()
    try:
        width, height = read_header(blob)
    except BadEntry as problem:
        fail(str(problem))

    raw_out = os.environ.get("MAKEFUN_OUTPUT_DIR") or str(FALLBACK_DIR)
    out_dir = Path(raw_out)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(blob)
    # Read the copy back: the judge must receive exactly the bytes
    # stored in this repository, so confirm the write before reporting
    # success.
    if target.read_bytes() != blob:
        fail(f"wrote the wrong bytes to {target}")
    print(f"main.py: wrote {target} ({width}x{height}, {len(blob)} bytes)")


if __name__ == "__main__":
    deliver()
