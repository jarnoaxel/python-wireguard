from ctypes import *
import re
import os

dirname = os.path.dirname(os.path.realpath(__file__))
c_library = CDLL(dirname + '/bin/py-wireguard.so')

def valid_interface(interface):
    '''
    Validate the name of a network interface.
    '''
    return bool(re.match("^[A-Za-z0-9_-]*$", interface))

def empty_key():
    '''
    Create an empty key. Used for generating new keys, you should not need this.
    '''
    return create_string_buffer(b'\000' * 32)

def key_pair():
    '''
    Create a private/public key pair fo ruse with Wireguard.
    '''
    private, public = empty_key(), empty_key()
    c_library.generate_private_key(private)
    c_library.generate_public_key(private, public)
    return private, public

def create_server(name, port, private_key, local_ip):
    '''
    Create a server-side Wireguard interface. This is a Wireguard instance that listens on a port
    to allow clients to connect.
    '''
    if (valid_interface(name)):
        c_library.add_server_device(name.encode(), c_ushort(port), private_key)
        os.system("ip a add dev {} {}".format(name, local_ip))
    else:
        print("invalid device name '{}'".format(device))

def create_client(name, private_key, local_ip):
    '''
    Create a client-side Wireguard interface. This means that it won't be listening on a port.
    '''
    if (valid_interface(name)):
        c_library.add_client_device(name.encode(), private_key)
        os.system("ip a add dev {} {}".format(name, local_ip))
    else:
        print("invalid device name '{}'".format(device))

def client_add_peer(device_name, public_key, address, port):
    '''
    Add a 'peer' to a client-side setup. This means that the server will be added for this setup.
    '''
    c_library.add_server_peer(device_name.encode(), public_key, address.encode(), c_ushort(port))

def setup_client_connection(device_name, own_private, local_ip, srv_public, dest_address, dest_port):
    '''
    Connect to a Wireguard server as a client machine.
    :device_name:   The name of the interface that will be added.
    :own_private:   The private key used for creating the WireGuard network interface.
    :local_ip:      The local IP you will use. Should be provided by the server.
    :srv_public:    The public key of the Wireguard server.
    :dest_address:  The endpoint Wireguard will connect to.
    :dest_port:     The port used by the Wireguard server.
    '''
    create_client(device_name, own_private, local_ip)
    client_add_peer(device_name, srv_public, dest_address, dest_port)

def server_add_peer(device_name, public_key, local_ip):
    '''
    Add a client
    '''
    c_library.add_client_peer(device_name.encode(), public_key, local_ip.encode())

def delete_device(name):
    c_library.delete_device(name.encode())

def list_devices():
    c_library.list_devices()

def print_key(key):
    c_library.print_key(key)

def key_to_base64(key):
    str_val = create_string_buffer(b'\000' * 44)
    c_library.key_to_string(key, str_val)
    return str_val.value.decode()

def key_from_base64(base64):
    key = empty_key()
    c_library.key_from_string(base64.encode(), key)
    return key

def enable_device(device):
    if (valid_interface(device)):
        os.system("ip link set up {}".format(device))
    else:
        print("invalid device '{}'".format(device))
