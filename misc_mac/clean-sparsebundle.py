from os import scandir, unlink
from os.path import join as pjoin
from sys import argv
import plistlib

with open(pjoin(argv[1], 'Info.plist'), 'rb') as f:
    sbinfo = plistlib.load(f)

blank = b'\0' * sbinfo['band-size']

with scandir(pjoin(argv[1], 'bands')) as it:
    for fn in it:
        with open(fn, 'rb') as f:
            data = f.read()
            if data == blank:
                unlink(fn.path)
