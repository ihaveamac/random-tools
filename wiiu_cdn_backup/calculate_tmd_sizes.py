#!/usr/bin/env python3

import glob
import struct
import sys

# {b'titleid': {b'contentindex': int(size)}}
titles = {}

tmds = glob.glob(sys.argv[1] + '/**/tmd.*', recursive=True)

for tmd_file in tmds:
    with open(tmd_file, 'rb') as tmd:
        tmd.seek(0x18C)
        titleid = tmd.read(0x8)
        tmd.seek(0x1DE)
        content_count = struct.unpack('>H', tmd.read(0x2))[0]
        tmd.seek(0xB04)
        chunk_records = tmd.read(0x30 * content_count)

        if titleid not in titles:
            titles[titleid] = {}

        # https://stackoverflow.com/questions/13673060/split-string-into-strings-by-length
        chunks, chunk_size = len(chunk_records), 0x30
        for chunk in [chunk_records[i:i + chunk_size] for i in range(0, chunks, chunk_size)]:
            content_id = chunk[0:4]
            content_size = struct.unpack('>Q', chunk[8:16])[0]
            titles[titleid][content_id] = content_size

size = 0

for title in titles:
    for content in titles[title]:
        size += titles[title][content]

print(size)
