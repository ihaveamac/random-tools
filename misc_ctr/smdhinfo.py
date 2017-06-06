#!/usr/bin/env python3

import struct
import sys

if len(sys.argv) == 1:
    sys.exit("smdhinfo.py icon.smdh")

def chk(flags, flag):
    return str(flags & flag != 0)  # this is ugly

def readsmdhname(fi, lang):
    print("  {} Short Description:".format(lang))
    print("    " + f.read(0x80).decode('utf-16').replace('\0', '').replace('\n', '\n > '))
    print("  {} Long Description:".format(lang))
    print("    " + f.read(0x100).decode('utf-16').replace('\0', '').replace('\n', '\n > '))
    print("  {} Publisher:".format(lang))
    print("    " + f.read(0x80).decode('utf-16').replace('\0', '').replace('\n', '\n > '))

with open(sys.argv[1], 'rb') as f:
    print("Magic:  " + f.read(0x4).decode('utf-8'))
    print("Version:  {:04x}".format(struct.unpack("<H", f.read(0x2))[0]))
    print("Reserved (unknown):  {:04x}".format(struct.unpack("<H", f.read(0x2))[0]))

    # f.seek(0x208)
    print("Application titles:")
    readsmdhname(f, "Japanese")
    readsmdhname(f, "English")
    readsmdhname(f, "French")
    readsmdhname(f, "German")
    readsmdhname(f, "Italian")
    readsmdhname(f, "Spanish")
    readsmdhname(f, "Simplified Chinese")
    readsmdhname(f, "Korean")
    readsmdhname(f, "Dutch")
    readsmdhname(f, "Portuguese")
    readsmdhname(f, "Russian")
    readsmdhname(f, "Traditional Chinese")
    # readsmdhname(f, "Unknown")
    # readsmdhname(f, "Unknown")
    # readsmdhname(f, "Unknown")
    # readsmdhname(f, "Unknown")

    # f.seek(0x2008)
    ratings = struct.unpack("<" + ("B" * 16), f.read(0x10))
    print("\nRegional age ratings:")
    print(" > CERO (Japan):         {0:3d} (0x{0:02x})".format(ratings[0x0]))
    print(" > ESRB (USA):           {0:3d} (0x{0:02x})".format(ratings[0x1]))
    print(" > Reserved (0x200a):    {0:3d} (0x{0:02x})".format(ratings[0x2]))
    print(" > USK (German):         {0:3d} (0x{0:02x})".format(ratings[0x3]))
    print(" > PEGI GEN (Europe):    {0:3d} (0x{0:02x})".format(ratings[0x4]))
    # print(" > Reserved (0x200d):    {0:3d} (0x{0:02x})".format(ratings[0x5]))
    print(" > PEGI PRT (Portugal):  {0:3d} (0x{0:02x})".format(ratings[0x6]))
    print(" > PEGI BBFC (England):  {0:3d} (0x{0:02x})".format(ratings[0x7]))
    print(" > COB (Australia):      {0:3d} (0x{0:02x})".format(ratings[0x8]))
    print(" > GRB (South Korea):    {0:3d} (0x{0:02x})".format(ratings[0x9]))
    print(" > CGSRR (Taiwan):       {0:3d} (0x{0:02x})".format(ratings[0xA]))
    # print(" > Reserved (0x2013):    {0:3d} (0x{0:02x})".format(ratings[0xB]))
    # print(" > Reserved (0x2014):    {0:3d} (0x{0:02x})".format(ratings[0xC]))
    # print(" > Reserved (0x2015):    {0:3d} (0x{0:02x})".format(ratings[0xD]))
    # print(" > Reserved (0x2016):    {0:3d} (0x{0:02x})".format(ratings[0xE]))
    # print(" > Reserved (0x2017):    {0:3d} (0x{0:02x})".format(ratings[0xF]))

    # f.seek(0x2018)
    regionlockout = struct.unpack("<I", f.read(0x4))[0]
    print("\nRegion lockout:  0x{:08x}".format(regionlockout))
    if regionlockout == 0x7FFFFFFF:
        print(" > Region free")
    else:
        print(" > Japan:               " + chk(regionlockout, 0x01))
        print(" > North America:       " + chk(regionlockout, 0x02))
        print(" > Europe:              " + chk(regionlockout, 0x04))
        print(" > Australia (unused):  " + chk(regionlockout, 0x08))
        print(" > China:               " + chk(regionlockout, 0x10))
        print(" > Korea:               " + chk(regionlockout, 0x20))
        print(" > Taiwan:              " + chk(regionlockout, 0x40))

    # f.seek(0x201C)
    matchmakerids = struct.unpack("<IQ", f.read(0xC))
    print("\nMatch Maker IDs:")
    print(" > ID:      0x{:08x}".format(matchmakerids[0x0]))
    print(" > BIT ID:  0x{:016x}".format(matchmakerids[0x1]))

    # f.seek(0x2028)
    flags = struct.unpack("<I", f.read(0x4))[0]
    print("\nFlags:  0x{:08x}".format(flags))
    print(" > Visibility:           " + chk(flags, 0x0001))
    print(" > Auto-boot gamecard:   " + chk(flags, 0x0002))
    print(" > Allow 3D:             " + chk(flags, 0x0004))
    print(" > Require EULA:         " + chk(flags, 0x0008))
    print(" > Autosave on exit:     " + chk(flags, 0x0010))
    print(" > Extended Banner:      " + chk(flags, 0x0020))
    print(" > Region game rating:   " + chk(flags, 0x0040))
    print(" > Use save data:        " + chk(flags, 0x0080))
    print(" > Record usage:         " + chk(flags, 0x0100))
    print(" > Unknown (0x0200):     " + chk(flags, 0x0200))
    print(" > Disable save backup:  " + chk(flags, 0x0400))
    print(" > Unknown (0x0800):     " + chk(flags, 0x0800))
    print(" > New 3DS exclusive:    " + chk(flags, 0x1000))
    print(" > Unknown (0x2000):     " + chk(flags, 0x2000))
    print(" > Unknown (0x4000):     " + chk(flags, 0x4000))
    print(" > Unknown (0x8000):     " + chk(flags, 0x8000))

    # f.seek(0x202C)
    eulaversion = struct.unpack(">BB", f.read(0x2))
    print("\nEULA Version:  {:d}.{:02d}".format(eulaversion[1], eulaversion[0]))

    # TODO: 'Optimal Animation Default Frame'

    # TODO: CEC ID (StreetPass)
