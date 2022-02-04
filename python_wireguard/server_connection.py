'''
Contains a class that represents a client-side peer, i.e. a connection to a server.
'''
class ServerConnection:
    '''
    A connection to a Wireguard server. Contains the public key of the server,
    and the endpoint IP and port.
    '''
    def __init__(self, public_key, host_ip, port):
        self.public_key = public_key
        self.host_ip = host_ip
        self.port = port

    def get_key(self):
        '''
        Get the public key of the server this points to.
        '''
        return self.public_key

    def get_endpoint(self):
        '''
        Get the destination IP.
        '''
        return self.host_ip

    def get_port(self):
        '''
        Get the server port.
        '''
        return self.port
