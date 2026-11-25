#!/usr/bin/env python3
"""Check that main.py is deterministic.

Runs main.py twice, each time in a fresh temporary directory, and
requires the two /output/entry.png copies to be byte-identical with the
same SHA-256. Standard library only.
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
# main.py always writes to the absolute /output directory; each run's
# bytes are read back immediately, before the next run overwrites them.
OUTPUT = "/output/entry.png"


def run_once(workdir):
    """Run main.py once in workdir; return the bytes it wrote."""
    shutil.copyfile(SOURCE, os.path.join(workdir, "entry.png"))
    result = subprocess.run(
        [sys.executable, MAIN_PY],
        cwd=workdir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        sys.exit(f"main.py failed in {workdir} (exit {result.returncode})")
    with open(OUTPUT, "rb") as handle:
        return handle.read()


def main():
    if not os.path.isfile(SOURCE):
        sys.exit("entry.png not found next to test_determinism.py")
    if not os.path.isfile(MAIN_PY):
        sys.exit("main.py not found next to test_determinism.py")

    results = []
    for i in range(2):
        with tempfile.TemporaryDirectory(prefix=f"determinism-run-{i + 1}-") as workdir:
            data = run_once(workdir)
            results.append(data)
            print(
                f"run {i + 1}: {len(data)} bytes, "
                f"sha256 {hashlib.sha256(data).hexdigest()}"
            )

    if results[0] != results[1]:
        sys.exit("FAIL: the two runs produced different bytes")
    print("PASS: both runs are byte-identical")


if __name__ == "__main__":
    main()
