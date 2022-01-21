#! /usr/bin/python3

import requests
import wireguard as wg

IP_ADDR = "209.97.176.198"
WG_PORT = 1234
HTTP_PORT = 8888
HTTP_FULL = "http://{}:{}".format(IP_ADDR, HTTP_PORT)

private, public = wg.key_pair()
public_string = wg.key_to_base64(public)

data = {
    'key': public_string
}

response = requests.post(url=HTTP_FULL, json=data).json()

srv_key = wg.key_from_base64(response['public_key'])
local_ip = response['ip']

wg.setup_client_connection('wg-client', private, "{}/24".format(local_ip), srv_key, IP_ADDR, WG_PORT)
wg.enable_device('wg-client')