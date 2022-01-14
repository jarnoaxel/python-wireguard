#!/usr/bin/python3

from wireguard import wg

print(wg.square(2))

wg.list_devices()

wg.add_device(b"testinterface", 1235)

wg.list_devices()