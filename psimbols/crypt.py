
import base64
import pyaes

import psimbols.err
    
class Crypt:

    def __init__(self):
        pass
        
    def encrypt_base64(self, string, client):
        encode_bytes = string.encode('utf-8')
        encrypted = self.encrypt_bytes(encode_bytes, client)
        
        base64_bytes = base64.b64encode(encrypted)
        return base64_bytes.decode('utf-8')
        
    def decrypt_base64(self, base64_string, client):
        base64_bytes = base64_string.encode('utf-8')
        decode_bytes = base64.b64decode(base64_bytes, validate=True)
        
        decrypted = self.decrypt_bytes(decode_bytes, client)
        return decrypted.decode('utf-8')
     
    def encrypt_bytes(self, bytes, client):
        return bytes
           
    def decrypt_bytes(self, bytes, client):
        return bytes
