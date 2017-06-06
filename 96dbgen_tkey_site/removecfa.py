#!/usr/bin/env python2
import glob
import os

for ncch in glob.glob("**/*.dec"):
    f = open(ncch, "rb")
    f.seek(0x150)
    productcode = f.read(10)
    #print(productcode)
    f.close()
    if productcode == "CTR-P-CTAP":
        print("removing %s" % ncch)
        os.remove(ncch)
