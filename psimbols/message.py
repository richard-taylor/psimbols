
class ClientUnauthorised(Exception):
    pass
    
class Processor:

    def process(self, message):
        if 'client' in message:
            return message
        raise ClientUnauthorised()
