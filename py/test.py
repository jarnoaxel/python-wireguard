#! /usr/bin/python3

import wireguard as wg;

private, public = wg.key_pair()

wg.list_devices()

wg.add_peer('wg_test', public)

wg.list_devices()
