'''
Contains a class representing a server-side Wireguard connection.
'''
import python_wireguard as wg
from .key import Key

class Server:
    '''
    This is a server-side Wireguard connection.
    '''
    def __init__(self, interface_name, key, local_ip, port):
        if not wg.valid_interface(interface_name):
            raise ValueError(f"Invalid interface name {interface_name}")
        if not isinstance(key, Key):
            raise ValueError("Key should be an instance of python_wireguard.Key")
        self.interface_name = interface_name
        self.key = key
        self.local_ip = local_ip
        self.port = port
        self.clients = []
        self.interface_created = False

    def create_interface(self):
        '''
        Create the network interface belonging to this wg server.
        '''
        wg.create_server(self.interface_name, self.port, self.key, self.local_ip)
        self.interface_created = True

    def delete_interface(self):
        '''
        Deletes the network interface of this server.
        '''
        wg.delete_device(self.interface_name)
        self.interface_created = False

    def add_client(self, client_connection):
        '''
        Add a new client to this server.
        '''
        wg.server_add_peer(self.interface_name,
                           client_connection.get_key(),
                           client_connection.get_ip())

    def enable(self):
        '''
        Turn on the network interface.
        '''
        if not self.interface_created:
            self.create_interface()
        wg.enable_device(self.interface_name)
