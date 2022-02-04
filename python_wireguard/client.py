'''
Contains a class representing a client-side Wireguard connection.
'''
from .wireguard import valid_interface, create_client, delete_device, client_add_peer, enable_device
from .key import Key
from .server_connection import ServerConnection

class Client:
    '''
    This is a client-side Wireguard connection.
    '''
    def __init__(self, interface_name, key, local_ip):
        if not valid_interface(interface_name):
            raise ValueError(f"Invalid interface name {interface_name}")
        if not isinstance(key, Key):
            raise ValueError("Key should be an instance of python_wireguard.Key")

        self.key = key
        self.local_ip = local_ip
        self.interface_name = interface_name
        self.connection = None
        self.interface_created = False

    def create_interface(self):
        '''
        Create the internet interface belonging to this client.
        '''
        create_client(self.interface_name, self.key.as_bytes(), self.local_ip)
        self.interface_created = True

    def delete_interface(self):
        '''
        Delete the internet interface belonging to this client.
        '''
        delete_device(self.interface_name)
        self.interface_created = False

    def set_server(self, server_connection):
        '''
        Set the server for this Client.
        '''
        if not isinstance(server_connection, ServerConnection):
            raise ValueError(
                "server_connection should be an instance of python_wireguard.ServerConnection"
                )
        self.connection = server_connection

    def connect(self):
        '''
        Connect to the Wireguard server.
        '''
        if not self.interface_created:
            self.create_interface()
        if self.connection is None:
            raise ValueError(
                "The connection has not been configured for this Client yet. \
                Use 'set_server' to set it."
                )
        server_connection = self.connection
        key = server_connection.get_key()
        client_add_peer(self.interface_name, key.as_bytes(),
            server_connection.get_endpoint(), server_connection.get_port())
        enable_device(self.interface_name)
