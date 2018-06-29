
import base64
import json

import psimbols.crypt
import psimbols.err
import psimbols.register

crypt = psimbols.crypt.Crypt()
register = psimbols.register.Register()
   
class Processor:

    def process(self, message):

        if 'client' not in message:
            raise psimbols.err.BadMessageFormat()

        client = register.get_client(message['client'])
        
        if client is None:
            raise psimbols.err.ClientUnauthorised()
        
        if 'request' not in message:
            raise psimbols.err.BadMessageFormat()

        request_string = message['request']
        request_base64 = request_string.encode('utf-8')
        request_binary = base64.b64decode(request_base64)
        
        plaintext = crypt.decrypt(request_binary, client)
        try:
            request = json.loads(plaintext)
            
        except json.JSONDecodeError:
            raise psimbols.err.ClientUnautorised()

        # now 'request' is the object to execute
        # if it has 'request_id' and 'run'
