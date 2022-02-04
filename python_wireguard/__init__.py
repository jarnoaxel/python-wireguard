'''
This module is a wrapper for interacting with Wireguard on Linux.
'''
from .wireguard import list_devices, delete_device
from .key import Key
from .client import Client
from .server_connection import ServerConnection
from .server import Server
from .client_connection import ClientConnection
