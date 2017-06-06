#!/usr/bin/env python2
import binascii
import json
import os
import stat
import urllib

# used from http://www.gossamer-threads.com/lists/python/python/163938
def bytes2int(string):
    i_s = 0
    for ch in string:
        i_s = 256 * i_s + ord(ch)
    return i_s

#urlthing = "https://{tkey_site}/json_dec"
#dectitlekeylist_json = urllib.urlopen(urlthing)
dectitlekeylist_json = open("files/json_dec", "rb")
dectitlekeylist = json.loads(dectitlekeylist_json.read())
dectitlekeylist_json.close()

seeddb = open("files/seeddb.bin", "rb")
seeddb_count = bytes2int(seeddb.read(2)[::-1])
#downloadsh = open("download_tmp.sh", "wb")
for c in range(0, seeddb_count):
    seeddb.seek((c * 32) + 16)
    tid = binascii.hexlify(seeddb.read(8)[::-1])
    if not os.path.isfile("files/9.6-dbgen-xmls/mmap/%s.xml" % tid.upper()):
        for e in dectitlekeylist:
            if e["titleID"] == tid:
                os.system("./files/PlaiCDN-mod.py %s %s -nobuild\n" % (tid, e["titleKey"]))
                #downloadsh.write("./files/PlaiCDN-mod.py %s %s -nobuild\n" % (tid, e["titleKey"]))

seeddb.close()
#downloadsh.close()
#st = os.stat("download_tmp.sh")
#os.chmod("download_tmp.sh", st.st_mode | stat.S_IEXEC)
