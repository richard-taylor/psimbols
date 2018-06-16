
import psimbols.err
    
class Processor:

    def process(self, message):

        if 'request' not in message:
            raise psimbols.err.BadMessageFormat()

        request = message['request']

        if 'channel' in message:
            return self.channel_request(message['channel'], request)

        if 'public_key' in message:
	        return self.channel_setup(message['public_key'], request)

        raise psimbols.err.BadMessageFormat()

    def channel_request(self, channel, request):
        return { "response": "got channel request" }

    def channel_setup(self, public_key, request):
        return { "response": "got channel setup" }
