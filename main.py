#!/usr/bin/env python3
"""Copy the finished news image to the grader output directory.

The image ships in this repository as entry.png. The copy lands at
$MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png by default) and is
checked to be a whole PNG under the 1 MiB limit. Standard library only.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576  # one mebibyte, the gate's size cap
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"  # the eight bytes every PNG starts with
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def check_png(path):
    """Return an error string, or None when path is a valid small PNG."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return "output is %d bytes, over the %d limit" % (size, MAX_BYTES)
    with open(path, "rb") as handle:
        head = handle.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        return "output lacks the PNG signature"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        return fail("source image %s is missing" % source)
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, OUTPUT_NAME)
    shutil.copyfile(source, dest)
    problem = check_png(dest)
    if problem is not None:
        return fail(problem)
    with open(dest, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (dest, os.path.getsize(dest), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
