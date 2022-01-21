#! /usr/bin/python3

import requests
import wireguard as wg
import sys
import os

WG_INTERFACE = 'wg-client'
PRINT_COMMANDS = False

def connect(hostname):
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

    wg.delete_device(WG_INTERFACE)
    wg.setup_client_connection(WG_INTERFACE, private, "{}/24".format(local_ip), srv_key, vpn_ip, vpn_port)
    wg.enable_device(WG_INTERFACE)
    
    execute_verbose("ip route add 0.0.0.0/1 dev {}".format(WG_INTERFACE))
    execute_verbose("ip route add ::/0 dev {}".format(WG_INTERFACE))
    execute_verbose("ip route add 128.0.0.0/1 dev {}".format(WG_INTERFACE))
    
    default_route = os.popen("ip route | grep default").read().split(' ')
    req_parts = ' '.join(default_route[2:5])
    
    execute_verbose("ip route add {}/32 via {}".format(vpn_ip, req_parts))

def disconnect():
    wg.delete_device(WG_INTERFACE)
    execute_verbose("ip route delete 0.0.0.0/1")
    execute_verbose("ip route delete 128.0.0.0/1")
    execute_verbose("ip route delete ::/0")

def execute_verbose(command):
    if PRINT_COMMANDS:
        print(command)
    os.system(command)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Usage: `{} connect 'server_address'` or ``".format(sys.argv[0]))
    
    command = sys.argv[1]
    
    if command == "connect":
        if len(sys.argv) < 3:
            print("no host specified")
            exit(1)
        server_address = sys.argv[2]
        connect(server_address)
    elif command == "disconnect":
        disconnect()
    else:
        print("unknown command {}".format(command))
