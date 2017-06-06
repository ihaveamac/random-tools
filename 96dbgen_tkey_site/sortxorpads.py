#!/usr/bin/env python2
import glob
import os

try:
    os.remove("ncchinfo.bin")  # trying to keep the folder clean I guess
except OSError:
    if os.path.isfile("ncchinfo.bin"):
        raise

for d in glob.glob("0004*/"):
    tid = d[:-1].upper()
    print(tid)
    if os.path.isfile("%s.Main.exefs_norm.xorpad" % tid):
        print("exefs_norm xorpad found")
        os.rename("%s.Main.exefs_norm.xorpad" % tid, "%s/%s.Main.exefs_norm.xorpad" % (tid.lower(), tid))
    if os.path.isfile("%s.Main.exefs_7x.xorpad" % tid):
        print("exefs_7x xorpad found")
        os.rename("%s.Main.exefs_7x.xorpad" % tid, "%s/%s.Main.exefs_7x.xorpad" % (tid.lower(), tid))
