
import psimbols.client

class DummyCrypt:
    def encrypt_base64(self, text, client):
        return text
    def decrypt_base64(self, text, client):
        return text

class DummyRegister:
    def get_client(self, id):
        if id == '123':
            return psimbols.client.Client(id, 'localhost', b'1234567890123456')

