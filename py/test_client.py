#! /usr/bin/python3

import requests
import wireguard as wg
import sys

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: {} 'server_address'".format(sys.argv[0]))
    
    server_address = sys.argv[1]

    private, public = wg.key_pair()
    public_string = wg.key_to_base64(public)

    data = {
        'key': public_string
    }

    response = requests.post(url=server_address, json=data).json()

    srv_key = wg.key_from_base64(response['public_key'])
    local_ip = response['ip']
    vpn_ip = response['vpn_ip']
    vpn_port = response['vpn_port']

    wg.delete_device('wg-client')
    wg.setup_client_connection('wg-client', private, "{}/24".format(local_ip), srv_key, vpn_ip, vpn_port)
    wg.enable_device('wg-client')