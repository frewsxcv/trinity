#!/usr/bin/env python3
# Copyright © 2026 CCP ehf.

"""Convert TrinityALTest screenshots to PNG.

TrinityALTest --screenshots writes the back buffer as .dds files, but the header
it writes is the small variant declared in WithValidRenderContextFixture.cpp
rather than a standard DDS header, so most image viewers reject the result. This
converts them to PNG so a run can actually be looked at.

    TrinityALTest_metal --screenshots --screenshotdir shots --gtest_filter=Rendering.*
    python3 dds2png.py shots/metal/Rendering/*.dds
"""

import argparse
import os
import struct
import sys
import zlib

# WithValidRenderContextFixture.cpp writes DDS_HEADER, which is 128 bytes:
# 8 uint32 fields, uint32 reserved1[11], DDS_PIXELFORMAT (8 uint32),
# 2 uint32 flags, uint32 reserved2[3].
HEADER_SIZE = 128
DDS_MAGIC = 0x20534444  # 'DDS ' little-endian


def read_dds(path):
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < HEADER_SIZE:
        raise ValueError("file is too small to hold a header")

    magic, _size, _flags, height, width = struct.unpack_from("<5I", data, 0)
    if magic != DDS_MAGIC:
        raise ValueError("not a TrinityALTest screenshot (bad magic %#x)" % magic)
    if width == 0 or height == 0:
        raise ValueError("header reports an empty image")

    body = data[HEADER_SIZE:]
    # The fixture writes pitch * height bytes, and pitch may exceed width * 4.
    pitch = len(body) // height
    if pitch < width * 4:
        raise ValueError("truncated pixel data")

    return width, height, pitch, body


def to_png(path, out_path):
    width, height, pitch, body = read_dds(path)

    # The fixture declares B at the low byte and forces alpha opaque, so each
    # pixel is stored BGRA. PNG truecolour wants RGB.
    scanlines = []
    for y in range(height):
        row = body[y * pitch:y * pitch + width * 4]
        pixels = bytearray(b"\x00")  # PNG filter type 0
        for x in range(width):
            b, g, r = row[x * 4], row[x * 4 + 1], row[x * 4 + 2]
            pixels += bytes((r, g, b))
        scanlines.append(bytes(pixels))

    def chunk(tag, payload):
        body = tag + payload
        return (struct.pack(">I", len(payload)) + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(b"".join(scanlines), 9))
    png += chunk(b"IEND", b"")

    with open(out_path, "wb") as f:
        f.write(png)

    return width, height


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", help="screenshot .dds files")
    parser.add_argument("-o", "--outdir", help="write PNGs here instead of alongside the input")
    args = parser.parse_args()

    if args.outdir:
        os.makedirs(args.outdir, exist_ok=True)

    failures = 0
    for path in args.files:
        if args.outdir:
            out_path = os.path.join(args.outdir,
                                    os.path.splitext(os.path.basename(path))[0] + ".png")
        else:
            out_path = os.path.splitext(path)[0] + ".png"
        try:
            width, height = to_png(path, out_path)
        except (OSError, ValueError) as exc:
            print("%s: %s" % (path, exc), file=sys.stderr)
            failures += 1
            continue
        print("%s  %dx%d" % (out_path, width, height))

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
