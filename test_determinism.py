"""Test: main.py writes the same bytes on two runs.

Run from the final/ directory:
    python3 test_determinism.py

Exits 0 on pass, 1 on failure. Uses only the standard library.
"""
import hashlib
import os
import subprocess
import sys
import tempfile


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with tempfile.TemporaryDirectory() as tmp:
        out1 = os.path.join(tmp, "run1.png")
        out2 = os.path.join(tmp, "run2.png")
        for out in (out1, out2):
            r = subprocess.run(
                [sys.executable, os.path.join(here, "main.py"), out],
                capture_output=True, text=True)
            if r.returncode != 0:
                print("FAIL: main.py exit", r.returncode, r.stderr)
                return 1
        s_src, s1, s2 = sha256(src), sha256(out1), sha256(out2)
        print("source:", s_src)
        print("run1:  ", s1)
        print("run2:  ", s2)
        if s_src == s1 == s2:
            print("PASS: two runs are byte-identical to the source image")
            return 0
        print("FAIL: outputs differ")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
