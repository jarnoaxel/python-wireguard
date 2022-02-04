class ServerConnection:
    def __init__(self, public_key, host_ip, port):
        self.public_key = public_key
        self.host_ip = host_ip
        self.port = port
    
    def get_key(self):
        return self.public_key
    
    def get_endpoint(self):
        return self.host_ip

    def get_port(self):
        return self.port