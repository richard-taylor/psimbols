
import base64

import psimbols.err
    
class Crypt:

    def __init__(self):
        pass
        
    def encrypt_b64(self, message):
        pass
        
    def decrypt_base64(self, base64_string, client):
        base64_bytes = base64_string.encode('utf-8')
        decode_bytes = base64.b64decode(base64_bytes)
        
        return self.decrypt_bytes(decode_bytes, client)
        
    def decrypt_bytes(self, bytes, client):
        return bytes
