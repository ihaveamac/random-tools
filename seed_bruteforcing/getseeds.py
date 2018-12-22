#!/usr/bin/env python2

from __future__ import print_function
import threading
import os
import urllib2
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

regionStrings = ["JP", "US", "GB", "HK", "KR", "TW"]

class myThread (threading.Thread):
	def __init__(self, start_offset, end_offset):
		threading.Thread.__init__(self)
		self.start_offset = start_offset
		self.end_offset = end_offset
	def run(self):
		forloop(self.start_offset, self.end_offset)

seeddir = "seeds"

def f(title, CC):
	try:
		seed = urllib2.urlopen(urllib2.Request("https://kagiya-ctr.cdn.nintendo.net/title/0x000400000%05X00/ext_key?country=%s" % (title, CC))).read()
		with open("seeds/000400000%05X00.dat" % title ,"wb") as o:
			o.write(seed)
		return 1
		print("got seed:       000400000%05X00\n" % title, end='')
	except urllib2.HTTPError:
		return 0

def seed(uid):
	uid_f = "000400000%05X00" % uid
	if os.path.isfile("seeds/000400000%05X00.dat" % uid):
		print("already exists: %s\n" % uid_f, end='')
	else:
		print("attempting:     %s\n" % uid_f, end='')
		for regionStrings_index in range(len(regionStrings)):
			try:
				ret = f(uid, regionStrings[regionStrings_index])
				if ret == 1: break
			except Exception as e:
				print('failed to get seed for %s %s: %s: %s' % (regionStrings[regionStrings_index], uid_f, type(e).__name__, e))

def forloop(start, end):
	for uid_r in range(start, end):
		seed(uid_r)

print("Downloading seeds from CDN...")
if not os.path.isdir(seeddir):
    os.mkdir(seeddir)

myThread(0, 0x800).start()
myThread(0x800, 0x1000).start()
myThread(0x1000, 0x1800).start()
myThread(0x1800, 0x2000).start()
myThread(0xf7000, 0xf7800).start()
myThread(0xf7800, 0xf8000).start()
