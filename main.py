#!/usr/bin/env python3
"""Entry point for the 'Sum up 24 November's world news in one image' entry.

Copies the bundled front-page image (entry.png, sitting next to this file)
to /output/entry.png. Standard library only, no network, deterministic:
the output is a byte-for-byte copy of the input.

Usage:
    python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = "/output"
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")

MAX_BYTES = 1024 * 1024  # 1 MiB
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def png_dimensions(path: str) -> tuple:
    """Return (width, height) from a PNG file's IHDR chunk, stdlib only."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG file: {path}")
    if header[12:16] != b"IHDR":
        raise ValueError(f"PNG missing IHDR chunk: {path}")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1
    try:
        width, height = png_dimensions(SOURCE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(
            f"error: {SOURCE} is {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}",
            file=sys.stderr,
        )
        return 1
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(
            f"error: {SOURCE} is {size} bytes, over the {MAX_BYTES} byte limit",
            file=sys.stderr,
        )
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"copied {SOURCE} -> {OUTPUT}")
    print(f"size: {size} bytes, dimensions: {width}x{height}")
    print(f"sha256: {sha256_file(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
