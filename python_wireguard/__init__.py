'''
This module is a wrapper for interacting with Wireguard on Linux.
'''
from .wireguard import valid_interface, empty_key, key_pair, create_server, create_client, client_add_peer, setup_client_connection, server_add_peer, delete_device, list_devices, print_key, key_to_base64, key_from_base64, enable_device
from .key import Key
from .client import Client
from .server_connection import ServerConnection
