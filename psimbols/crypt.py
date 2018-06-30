
import base64
import os
import pyaes
    
class Crypt:

    def __init__(self):
        pass
        
    def encrypt_base64(self, string, client):
        encode_bytes = string.encode('utf-8')
        encrypted = self.encrypt_bytes(encode_bytes, client)
        
        base64_bytes = base64.b64encode(encrypted)
        return base64_bytes.decode('utf-8')
        
    def decrypt_base64(self, string, client):
        base64_bytes = string.encode('utf-8')
        decode_bytes = base64.b64decode(base64_bytes, validate=True)
        
        decrypted = self.decrypt_bytes(decode_bytes, client)
        return decrypted.decode('utf-8')
     
    def encrypt_bytes(self, plaintext, client):
    
        # use a random initialisation vector
        iv = os.urandom(16)
        
        cbc = pyaes.AESModeOfOperationCBC(client.key, iv=iv)
        encrypter = pyaes.Encrypter(cbc)

        ciphertext = encrypter.feed(plaintext)
        ciphertext += encrypter.feed()
        
        # prepend the initialisation vector
        return iv + ciphertext
        
    def decrypt_bytes(self, bytes, client):
        
        # expect at least the iv and one block
        if len(bytes) < 32:
            raise ValueError()
            
        # detach the initialisation vector
        iv = bytes[0:16]
        ciphertext = bytes[16:]
        
        cbc = pyaes.AESModeOfOperationCBC(client.key, iv=iv)
        decrypter = pyaes.Decrypter(cbc)

        plaintext = decrypter.feed(ciphertext)
        plaintext += decrypter.feed()
        
        return plaintext
