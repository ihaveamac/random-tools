#!/usr/bin/env python3
import subprocess as sp
from os.path import exists, expanduser
from sys import argv
from datetime import datetime

from Foundation import NSUserNotification
from Foundation import NSUserNotificationCenter
from Foundation import NSUserNotificationDefaultSoundName


# https://stackoverflow.com/questions/17651017/python-post-osx-notification
def notify(_title, _message, _sound = False):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(_title)
    notification.setInformativeText_(_message)
    if _sound == True:
        notification.setSoundName_(NSUserNotificationDefaultSoundName)

    center = NSUserNotificationCenter.defaultUserNotificationCenter()
    center.deliverNotification_(notification)


battery_info = sp.check_output(['ioreg', '-rc', 'AppleSmartBattery'], encoding='utf-8')
now = datetime.now()

charging = None
for l in battery_info.splitlines():
    if '"ExternalChargeCapable"' in l:
        charging = l.split()[-1] != 'No'
    elif '"MaxCapacity"' in l:
        maximum = int(l.split()[-1])
    elif '"CurrentCapacity"' in l:
        current = int(l.split()[-1])

print('DateTime:', str(now))
print('Charging:', charging)
print('Maximum:', maximum)
print('Current:', current)

needs_unplugging = current / maximum
if charging:
    print('Currently charging.')
    if needs_unplugging >= 0.95:
        print('Needs unplugging. (%f)' % (needs_unplugging))
        notify('Battery charged', 'Charger should now be disconnected.')
    else:
        print('Does not need unplugging. (%f)' % (needs_unplugging))
else:
    print('Not charging. (%f)' % (needs_unplugging))

if 'log' in argv:
    out = expanduser('~/Library/Logs/Battery Log.csv')
    if not exists(out):
        with open(out, 'w') as f:
            f.write('DateTime,Charging,Maximum,Current\n')
    with open(out, 'a') as f:
        f.write('%s,%s,%i,%i\n' % (now, charging, maximum, current))
        print('Wrote log to', out)
