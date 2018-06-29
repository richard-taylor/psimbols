
import psimbols.client
import psimbols.err
    
class Register:

    def get_client(self, id):

        if id == '123':
            return psimbols.client.Client('123', 'localhost:9393', '789')
        return None
