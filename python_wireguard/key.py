'''
Python class for using a Wireguard public or private key.
'''
import python_wireguard.wireguard as wg

class Key:
    '''
    This represents a Wireguard key.
    '''
    def __init__(self, base64_string=None):
        if base64_string is None:
            self.byte_content = wg.empty_key()
        elif len(base64_string) != 44:
            raise ValueError("Invalid base64 string provided")
        else:
            self.byte_content = wg.key_from_base64(base64_string)

    def __str__(self):
        '''
        Convert this key to a string.
        '''
        return wg.key_to_base64(self.byte_content)

    def __repr__(self):
        '''
        Represent this class (used in the python cli).
        '''
        return f"<python_wireguard.Key object: {str(self)}>"

    @staticmethod
    def key_pair():
        '''
        Create a new private/public key pair.
        '''
        private, public = wg.key_pair()
        private_obj = Key(wg.key_to_base64(private))
        public_obj = Key(wg.key_to_base64(public))
        return private_obj, public_obj

    def as_bytes(self):
        '''
        Get the c_char_array content of this key.
        '''
        return self.byte_content
