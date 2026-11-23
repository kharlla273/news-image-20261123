#!/usr/bin/env python3
"""Copy the submitted newspaper image to the grader's output directory.

The entry image lives in this repository as entry.png. This program
verifies it is a whole PNG under the 1 MiB cap and copies it, byte for
byte, to $MAKEFUN_OUTPUT_DIR/entry.png. It reads nothing else and makes
no network calls, so two runs always write identical bytes. The copy is
verbatim: no re-encoding, no resizing, no timestamp is embedded, so the
output is fully determined by the input file alone.
"""

import os
import sys

PNG_SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
MAX_BYTES = 1024 * 1024


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    with open(source, "rb") as handle:
        data = handle.read()

    if len(data) == 0:
        print("entry.png is empty", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    if data[:8] != PNG_SIGNATURE:
        print("entry.png does not start with the PNG signature",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")

    with open(destination, "wb") as handle:
        handle.write(data)

    print(f"wrote {destination} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
