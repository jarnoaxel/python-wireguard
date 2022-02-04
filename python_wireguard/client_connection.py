'''
Contains a class that represents a server-side peer, i.e. a connection to a client.
'''
class ClientConnection:
    '''
    A connection to a Wireguard client. Contains the public key of the client,
    and the local IP of the client.
    '''
    def __init__(self, public_key, local_ip):
        self.public_key = public_key
        self.local_ip = local_ip

    def get_key(self):
        '''
        Get the public key of the client this points to.
        '''
        return self.public_key

    def get_ip(self):
        '''
        Get the local IP.
        '''
        return self.local_ip
