
import psimbols.client
import psimbols.err

ID = '123'
KEY = b'ABCDEFGHIJKLMNOPQRSTUVWX'

class Register:

    def get_client(self, id):

        if id == '123':
            return psimbols.client.Client(ID, 'localhost:9393', KEY)
        return None
