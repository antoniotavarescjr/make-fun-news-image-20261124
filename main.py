"""Sum up 24 November's world news in one image.

Writes the final image to /output/entry.png by copying the image this
repository holds. No network, no randomness, no timestamps in the output:
two runs write the same bytes.
"""
import hashlib
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(src, out)
    digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("wrote " + out + " sha256=" + digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
