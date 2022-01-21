from ctypes import *
import re
import os

c_library = CDLL('../c/library.so')

def valid_interface(interface):
    return bool(re.match("^[A-Za-z0-9_-]*$", interface))

def empty_key():
    return create_string_buffer(b'\000' * 32)

def key_pair():
    private, public = empty_key(), empty_key()
    c_library.generate_private_key(private)
    c_library.generate_public_key(private, public)
    return private, public

def create_server(name, port, private_key, local_ip):
    if (valid_interface(name)):
        c_library.add_device(name.encode(), c_ushort(port), private_key)
        os.system("ip a add dev {} {}".format(name, local_ip))
    else:
        print("invalid device name '{}'".format(device))

def create_client(name, private_key, local_ip):
    if (valid_interface(name)):
        c_library.add_device(name.encode(), c_ushort(port), private_key)
        os.system("ip a add dev {} {}".format(name, local_ip))
    else:
        print("invalid device name '{}'".format(device))

def client_add_peer(device_name, public_key, address, port):
    c_library.add_server_peer(device_name.encode(), public_key, address.encode(), c_ushort(port))

def setup_client_connection(device_name, own_private, local_ip, srv_public, dest_address, dest_port):
    create_client(device_name, own_private, local_ip)
    client_add_peer(device_name, srv_public, dest_address, dest_port)

def server_add_peer(device_name, public_key, address):
    c_library.add_client_peer(device_name.encode(), public_key, address.encode())

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