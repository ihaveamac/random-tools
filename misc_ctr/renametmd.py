#!/usr/bin/env python3

import glob
import struct
import os

for tmd_name in glob.glob("./**/tmd"):
    with open(tmd_name, 'rb') as tmd:
        tmd.seek(0x1DC)
        version = struct.unpack(">H", tmd.read(0x2))[0]
    os.rename(tmd_name, "{}.{}".format(tmd_name, version))
