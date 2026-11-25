#!/usr/bin/env python3
"""Copy the v2 front-page image to /output/entry.png and validate it.

The image itself (entry.png) is generated separately; this program only
checks that it is a well-formed 1024x1024 PNG of at most 1 MiB, copies it
to /output/entry.png, and prints its SHA-256 so the result can be checked
against the submitted file. Standard library only, no network.
"""

import binascii
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(DEST_DIR, "entry.png")

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # 1 MiB


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_png_header(data):
    """Return (width, height) from the IHDR chunk of a PNG byte string."""
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        fail("entry.png is not a PNG file (bad signature)")
    if len(data) < 33:
        fail("entry.png is too short to contain an IHDR chunk")
    chunk_length = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or chunk_length != 13:
        fail("entry.png has no valid IHDR chunk as its first chunk")
    stored_crc = struct.unpack(">I", data[29:33])[0]
    actual_crc = binascii.crc32(data[12:29]) & 0xFFFFFFFF
    if stored_crc != actual_crc:
        fail(
            f"entry.png IHDR chunk is corrupt (CRC {stored_crc:08x}, "
            f"expected {actual_crc:08x})"
        )
    width, height = struct.unpack(">II", data[16:24])
    bit_depth = data[24]
    color_type = data[25]
    # Valid (color type, bit depth) pairs per the PNG specification.
    # The generated image may be palette-based (type 3), so every legal
    # combination is accepted; only malformed headers are rejected.
    valid_depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
                    4: (8, 16), 6: (8, 16)}
    if color_type not in valid_depths or bit_depth not in valid_depths[color_type]:
        fail(
            f"entry.png has invalid IHDR color type {color_type} with "
            f"bit depth {bit_depth}"
        )
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        fail(
            f"{SOURCE} not found next to main.py; "
            f"the image must sit next to main.py"
        )

    with open(SOURCE, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        fail(
            f"entry.png is {len(data)} bytes, over the 1 MiB limit "
            f"({MAX_BYTES} bytes)"
        )

    width, height = read_png_header(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(
            f"entry.png is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )

    os.makedirs(DEST_DIR, exist_ok=True)
    with open(DEST, "wb") as handle:
        handle.write(data)

    # Re-read what was written and confirm it is byte-identical.
    with open(DEST, "rb") as handle:
        written = handle.read()
    if written != data:
        fail(f"{DEST} does not match {SOURCE} after writing")

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {DEST} ({len(data)} bytes, {width}x{height})")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
