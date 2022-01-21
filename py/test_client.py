#! /usr/bin/python3

import requests
import wireguard as wg
import sys

IP_ADDR = "209.97.176.198"
WG_PORT = 1234
HTTP_PORT = 8888
HTTP_FORMAT = "http://{}:{}"

if __name__ == '__main__':

    private, public = wg.key_pair()
    public_string = wg.key_to_base64(public)

    data = {
        'key': public_string
    }

    endpoint = HTTP_FORMAT.format(IP_ADDR, HTTP_PORT)
    response = requests.post(url=HTTP_FULL, json=data).json()

    srv_key = wg.key_from_base64(response['public_key'])
    local_ip = response['ip']

    wg.delete_device('wg-client')
    wg.setup_client_connection('wg-client', private, "{}/24".format(local_ip), srv_key, IP_ADDR, WG_PORT)
    wg.enable_device('wg-client')