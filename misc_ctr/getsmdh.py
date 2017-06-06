#!/usr/bin/env python3

import binascii
import glob
import struct
import sys

def roundup(x):
    return ( (x + 63) >> 6) << 6

mu = 0x200

print("getting cias")
cias = glob.glob("./**/*.cia", recursive=True)

for cia in cias:
    with open(cia, 'rb') as f:
        contentoffset = 0
        f.seek(0x0)  # Archive header
        contentoffset += roundup(struct.unpack("<I", f.read(0x4))[0])
        f.seek(0x8)  # Certificate chain
        contentoffset += roundup(struct.unpack("<I", f.read(0x4))[0])
        f.seek(contentoffset + 0x1DC)
        print(f.tell())
        tid = binascii.hexlify(f.read(0x8)).upper()
        f.seek(0xC)  # Ticket
        contentoffset += roundup(struct.unpack("<I", f.read(0x4))[0])
        f.seek(0x10)  # TMD
        contentoffset += roundup(struct.unpack("<I", f.read(0x4))[0])

        f.seek(contentoffset + 0x100)
        if f.read(0x4) != b'NCCH':
            print("NCCH magic not found, skipping... ({})".format(cia))
            continue
        f.seek(contentoffset + 0x18F)
        if ord(f.read(0x1)) & 4 == 0:
            print("NCCH not decrypted, skipping... ({})".format(cia))
            continue

        f.seek(contentoffset + 0x1A0)
        exefsoffset = struct.unpack("<I", f.read(0x4))[0] * mu
        contentoffset += exefsoffset
        f.seek(contentoffset)
        iconinfooffset = 0
        if f.read(0x8).strip(b'\0') == b'icon':
            print("icon found")
        else:
            f.seek(contentoffset + 0x10)
            if f.read(0x8).strip(b'\0') == b'icon':
                print("icon found")
                iconinfooffset += 0x10
            else:
                f.seek(contentoffset + 0x20)
                if f.read(0x8).strip(b'\0') == b'icon':
                    print("icon found")
                    iconinfooffset += 0x20
                else:
                    f.seek(contentoffset + 0x30)
                    if f.read(0x8).strip(b'\0') == b'icon':
                        print("icon found")
                        iconinfooffset += 0x30
                    else:
                        print("failed to find icon ({})".format(cia))
        f.seek(contentoffset + iconinfooffset + 0x8)
        contentoffset += 0x200 + struct.unpack("<I", f.read(0x4))[0]
        f.seek(contentoffset)
        if f.read(0x4) != b'SMDH':
            print("SMDH magic not found ({})".format(cia))
        f.seek(contentoffset)
        with open("/Users/ianburgwin/Desktop/{}.smdh".format(tid.decode('utf-8')), 'wb') as o:
            o.write(f.read(0x36C0))
