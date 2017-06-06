#!/usr/bin/env python2
import os
import binascii

seeddir = "seeds"

filestoadd = []
for file in os.listdir(seeddir):
    if len(file) == 20:
        filestoadd.append(file)

seeddb = open("seeddb.bin", "wb")
ts = list(format(len(filestoadd), 'x').rjust(4, '0'))
ts[::2], ts[1::2] = ts[1::2], ts[::2]
ts = "".join(ts)[::-1].ljust(32, '0')
ts = binascii.unhexlify(ts)
seeddb.write(ts)

for seedfile in filestoadd:
    seedfile_o = open("seeds/%s" % seedfile, "rb")
    s = list(seedfile[0:16])
    s[::2], s[1::2] = s[1::2], s[::2]
    s = binascii.unhexlify("".join(s)[::-1])
    s += seedfile_o.read().ljust(24, '\x00')
    seeddb.write(s)
    seedfile_o.close()

seeddb.close()
