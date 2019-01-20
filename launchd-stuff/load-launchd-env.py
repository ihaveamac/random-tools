#!/usr/bin/env python3
import plistlib
from argparse import ArgumentParser
from os.path import expanduser
from subprocess import run

p = ArgumentParser(description='Parse an environment plist.')
p.add_argument('plist', help='plist to read.', nargs='?', default=expanduser('~/.MacOSX/environment.plist'))

a = p.parse_args()

with open(a.plist, 'rb') as i:
    env = plistlib.load(i)

for k, v in env.items():
    print('Setting', k, 'to', v)
    run(['/bin/launchctl', 'setenv', k, v])
