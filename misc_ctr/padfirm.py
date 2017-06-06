#!/usr/bin/env python3

import sys
import os

if len(sys.argv) != 2:
    sys.exit("padfirm.py firm.bin")

filenamesplit = os.path.splitext(sys.argv[1])
filename = os.path.basename(filenamesplit[0])
fileext = filenamesplit[1]

with open("%s_padded%s" % (filename, fileext), "wb") as f:
    with open(sys.argv[1], "rb") as o:
        f.write(o.read().ljust(0x400000, b"\x00"))
