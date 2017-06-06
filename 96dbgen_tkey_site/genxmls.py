#!/usr/bin/env python2
import glob
import json
import os
import subprocess
import sys

def runcommand(cmdargs):
    proc = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    return proc.communicate()[0]

try:
    os.makedirs("xmls")
except OSError:
    if not os.path.isdir("xmls"):
        raise

dectitlekeylist_json = open("files/json_dec", "r")
dectitlekeylist = json.loads(dectitlekeylist_json.read().decode('utf-8'))
dectitlekeylist_json.close()

for title in glob.glob("0004*"):
    utitle = title.upper()
    print(utitle)
    os.chdir(title)
    decfile = glob.glob("*.dec")[0]
    runcommand(["3dstool", "-xvtf", "cxi", decfile, "--exefs", "exefs.bin", "--exefs-xor", "%s.Main.exefs_norm.xorpad" % utitle, "--exefs-top-xor", "%s.Main.exefs_7x.xorpad" % utitle])
    runcommand(["ctrtool", "-t", "exefs", "--exefsdir=exefs", "--decompresscode", "exefs.bin"])
    os.chdir("exefs")
    dbgen_xml = runcommand(["96crypto_dbgen.py", "code.bin"])
    os.chdir("../..")
    xml_file = open("xmls/%s.xml" % utitle, "w")
    for e in dectitlekeylist:
        if e["titleID"] == title:
            xml_file.write("<!-- {} ({}) -->\n{}".format(e["name"].encode('utf-8'), e["region"], dbgen_xml))
            break
    else:
        xml_file.write("<!-- GameName (REGION) -->\n%s" % dbgen_xml)
    xml_file.close()
