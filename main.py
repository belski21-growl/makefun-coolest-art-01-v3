"""Copy the bundled surrealist painting to the output directory.

The entry ships one image, art.png (a 1024x1024 JPEG of a colossal open
book floating on a midnight ocean, its pages turning into white birds).
This program validates the bytes and writes them to entry.png.
"""

import os
import sys

MAX_BYTES = 1048576
JPEG_MAGIC = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_art():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "art.png")
    with open(path, "rb") as f:
        return f.read()


def check(data):
    if not data:
        raise SystemExit("art.png is empty")
    if len(data) > MAX_BYTES:
        raise SystemExit("art.png exceeds 1 MiB")
    if data[:3] == JPEG_MAGIC:
        if data[-2:] != JPEG_END:
            raise SystemExit("JPEG is truncated: no end marker")
    elif data[:8] == PNG_MAGIC:
        pass
    else:
        raise SystemExit("art.png is neither JPEG nor PNG")
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    data = check(read_art())
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as f:
        f.write(data)
    with open(target, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("output mismatch: wrote %d bytes, read back %d"
                         % (len(data), len(written)))
    print("wrote %s (%d bytes)" % (target, len(data)))


if __name__ == "__main__":
    main()
