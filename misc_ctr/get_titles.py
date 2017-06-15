#!/usr/bin/env python3

import binascii
import glob
import struct

tmd_versions = {}

tmds = glob.glob('./**/*.tmd', recursive=True)
# print(tmds)
for tmd_file in tmds:
    with open(tmd_file, 'rb') as tmd:
        tmd.seek(0x18C)
        tid = binascii.hexlify(tmd.read(8)).decode('utf-8')
        tmd.seek(0x1DC)
        ver = struct.unpack('>H', tmd.read(2))[0]
        tmd_versions[tid] = ver

print(tmd_versions)
