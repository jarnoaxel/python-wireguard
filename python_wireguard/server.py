'''
Contains a class representing a server-side Wireguard connection.
'''
from .wireguard import valid_interface, create_server, delete_device, server_add_peer, enable_device
from .key import Key

class Server:
    '''
    This is a server-side Wireguard connection.
    '''
    def __init__(self, interface_name, key, local_ip, port):
        if not valid_interface(interface_name):
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
        create_server(self.interface_name, self.port, self.key.as_bytes(), self.local_ip)
        self.interface_created = True

    def delete_interface(self):
        '''
        Deletes the network interface of this server.
        '''
        delete_device(self.interface_name)
        self.interface_created = False

    def add_client(self, client_connection):
        '''
        Add a new client to this server.
        '''
        server_add_peer(self.interface_name,
                           client_connection.get_key().as_bytes(),
                           client_connection.get_ip())

    def enable(self):
        '''
        Turn on the network interface.
        '''
        if not self.interface_created:
            self.create_interface()
        enable_device(self.interface_name)
