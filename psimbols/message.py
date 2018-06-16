
import psimbols.err
    
class Processor:

    def process(self, message):
        if 'client' in message:
            return message
        raise psimbols.err.ClientUnauthorised()
