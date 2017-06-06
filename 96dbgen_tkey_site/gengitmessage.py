#!/usr/bin/env python2
import glob

for xml_name in glob.glob("xmls/*.xml"):
    xml = open(xml_name, "rb")
    gamename = xml.readline()[5:-5]
    xml.close()
    print("%s = %s" % (xml_name[5:-4], gamename))
