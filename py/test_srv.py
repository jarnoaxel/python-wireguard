#! /usr/bin/python3

# This is purely an example server, not to be used in production!
# See 'test_client.py' for connection instructions.

import os
import wireguard as wg
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from dotenv import load_dotenv
import os

load_dotenv()

HTTP_PORT = int(os.getenv('HTTP_PORT'))
WG_PORT = int(os.getenv('WG_PORT'))
PUBLIC_IP = os.getenv('SERVER_IP')
WG_INTERFACE = os.getenv('WG_INTERFACE')
IP_FORMAT = '10.0.0.{}'
INTERNET_INTERFACE = os.getenv('INTERNET_INTERFACE')

private, public = wg.key_pair()
public_string = wg.key_to_base64(public)
next_ip = 1

def get_next_ip():
    global next_ip
    next_ip += 1
    return next_ip

class VpnServer(BaseHTTPRequestHandler):
    next_ip = 2

    def _set_headers(self):
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        '''
        Return this to any POST request.
        '''
        print("received post")
        
        self.send_response(200)
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        
        data = json.loads(self.data_string)

        print(data['key'])
        ip = get_next_ip()
        ip_formatted = IP_FORMAT.format(ip)
        
        key = wg.key_from_base64(data['key'])
        
        wg.server_add_peer(WG_INTERFACE, key, ip_formatted)
        
        response = {
            'public_key': wg.key_to_base64(public),
            'ip': ip_formatted,
            'vpn_ip': PUBLIC_IP,
            'vpn_port': WG_PORT,
        }

        self.wfile.write(json.dumps(response).encode())

def run(server_class=HTTPServer, handler_class=VpnServer):
    server_address = ('', HTTP_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def setup_forwarding_rules():
    os.system("iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
    os.system("iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
    os.system("iptables -A INPUT -p udp -m udp --dport {} -m conntrack --ctstate NEW -j ACCEPT".format(WG_PORT))
    os.system("iptables -A INPUT -s {} -p tcp -m tcp --dport 53 -m conntrack --ctstate NEW -j ACCEPT".format(IP_FORMAT.format('0/24')))
    os.system("iptables -A INPUT -s {} -p udp -m udp --dport 53 -m conntrack --ctstate NEW -j ACCEPT".format(IP_FORMAT.format('0/24')))
    os.system("iptables -A FORWARD -i {} -o {} -m conntrack --ctstate NEW -j ACCEPT".format(WG_INTERFACE, WG_INTERFACE))
    os.system("iptables -t nat -A POSTROUTING -s {} -o {} -j MASQUERADE".format(IP_FORMAT.format('0/24'), INTERNET_INTERFACE))

if __name__ == '__main__':
    wg.delete_device(WG_INTERFACE)

    wg.create_server(WG_INTERFACE, WG_PORT, private, IP_FORMAT.format('1/24'))
    wg.enable_device(WG_INTERFACE)
    
    run()