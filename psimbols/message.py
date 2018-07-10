
import binascii
import json

import psimbols.crypt
import psimbols.err
import psimbols.register
import psimbols.runner

class Processor:

    def __init__(self, crypt=None, register=None, runner=None):
    
        if crypt is None:
            self.crypt = psimbols.crypt.Crypt()
        else:
            self.crypt = crypt
            
        if register is None:
            self.register = psimbols.register.Register()
        else:
            self.register = register
            
        if runner is None:
            self.runner = psimbols.runner.Runner()
        else:
            self.runner = runner
               
    def process(self, message):

        client = self.find_client(message)
        request = self.decode_request(message, client)
        
        result = self.run_request(request)
        response = self.encode_response(result, client)
        
        return {
            'client': client.id,
            'server': client.server,
            'response': response
        }
        
    def find_client(self, message):
        if 'client' not in message:
            raise psimbols.err.BadMessageFormat()

        client = self.register.get_client(message['client'])
        
        if client is None:
            raise psimbols.err.ClientUnauthorised()
            
        return client
        
    def decode_request(self, message, client):
        if 'request' not in message:
            raise psimbols.err.BadMessageFormat()

        try:
            plaintext = self.crypt.decrypt_base64(message['request'], client)
             
        except (binascii.Error, ValueError):
            raise psimbols.err.BadMessageFormat()
            
        try:
            return json.loads(plaintext)
               
        except json.JSONDecodeError:
            raise psimbols.err.ClientUnauthorised()
            
    def run_request(self, request):
        if 'run' not in request:
            raise psimbols.err.BadMessageFormat()
            
        result = self.runner.run(request['run'])
        
        if 'request_id' in request:
            result['request_id'] = request['request_id']
            
        return result
        
    def encode_response(self, result, client):
        plaintext = json.dumps(result)
        return self.crypt.encrypt_base64(plaintext, client)
        
        
