#!/usr/bin/env python3
"""Determinism test for the news-image-20261124 entry.

Runs main.py twice, each time in a fresh /output directory, and asserts
that the two outputs are byte-identical (same SHA-256) and equal to the
bundled entry.png. Standard library only.

Usage:
    python3 test_determinism.py
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(HERE, "main.py")
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = "/output"
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_once() -> str:
    """Run main.py once with a fresh output dir; return the output SHA-256."""
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    result = subprocess.run(
        [sys.executable, MAIN_PY],
        cwd=HERE,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"main.py failed with exit code {result.returncode}:\n"
            f"{result.stdout}{result.stderr}"
        )
    if not os.path.isfile(OUTPUT):
        raise AssertionError(f"main.py did not produce {OUTPUT}")
    return sha256_file(OUTPUT)


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"FAIL: source image not found: {SOURCE}", file=sys.stderr)
        return 1
    source_sha = sha256_file(SOURCE)
    print(f"source entry.png sha256: {source_sha}")

    sha1 = run_once()
    print(f"run 1 /output/entry.png sha256: {sha1}")
    sha2 = run_once()
    print(f"run 2 /output/entry.png sha256: {sha2}")

    if sha1 != sha2:
        print("FAIL: outputs differ between runs", file=sys.stderr)
        return 1
    if sha1 != source_sha:
        print("FAIL: output differs from bundled entry.png", file=sys.stderr)
        return 1
    print("PASS: two runs are byte-identical and match entry.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
