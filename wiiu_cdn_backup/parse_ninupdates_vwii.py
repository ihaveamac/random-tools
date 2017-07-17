#!/usr/bin/env python3

import binascii
import csv
import os
import struct
import sys
from urllib.request import urlretrieve

# {'titleid': ['ver', ...]}
titles = {}

with open(sys.argv[1], newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'TitleID':
            continue
        if row[0] not in titles:
            titles[row[0]] = []
        for version in row[2].split(' '):
            if version[1:] not in titles[row[0]]:
                titles[row[0]].append(version[1:])

for titleid in titles:
    print(titleid)
    os.makedirs('CDN/' + titleid, exist_ok=True)

    for version in titles[titleid]:
        print('  ' + version)

        tmd_path = titleid + '/tmd.' + version

        if not os.path.isfile('CDN/' + titleid + '/cetk'):
            urlretrieve('http://nus.cdn.c.shop.nintendowifi.net/ccs/download/' + titleid + '/cetk', 'CDN/' + titleid + '/cetk')
        if not os.path.isfile('CDN/' + titleid + '/tmd.' + version):
            urlretrieve('http://nus.cdn.c.shop.nintendowifi.net/ccs/download/' + tmd_path, 'CDN/' + tmd_path)

        with open('CDN/' + tmd_path, 'rb') as tmd:
            tmd.seek(0x1DE)
            content_count = struct.unpack('>H', tmd.read(0x2))[0]
            tmd.seek(0x1E4)
            chunk_records = tmd.read(0x24 * content_count)

        # https://stackoverflow.com/questions/13673060/split-string-into-strings-by-length
        chunks, chunk_size = len(chunk_records), 0x24
        for chunk in [chunk_records[i:i + chunk_size] for i in range(0, chunks, chunk_size)]:
            content_id = binascii.hexlify(chunk[0:4]).decode('utf-8')
            content_type = struct.unpack('>H', chunk[6:8])[0]
            print('    ' + content_id, end='      ')

            content_path = titleid + '/' + content_id

            if not os.path.isfile('CDN/' + content_path):
                print('downloading')
                urlretrieve('http://nus.cdn.c.shop.nintendowifi.net/ccs/download/' + content_path, 'CDN/' + content_path)
            else:
                print('')
