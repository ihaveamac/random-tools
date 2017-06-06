#!/usr/bin/env python3
import glob  # easiest thing I see
import json

total = 0
toprint = ""
for fn in glob.glob("info/0004*.txt"):
    total += 1
    with open(fn, "r") as f:
        titleinfo = json.load(f)
        toprint += "{0} | {1} | `{2}`\n".format(titleinfo[0].replace('\n', '<br>').replace('`', '\\`').replace('*', '\\*').replace('(', '\\(').replace(')', '\\)'), titleinfo[1], titleinfo[4])

print("This contains %i seeds of known titles.\n\nGame | Region | Title ID\n--- | --- | ---\n%s" % (total, toprint))

print("## Unknown titles\nSeeds for these exist, but info about the title ID is a mystery.\n\nTitle ID |\n--- |")
for fn in glob.glob("info_unknown/0004*.txt"):
    print("%s |" % fn[13:-4])
