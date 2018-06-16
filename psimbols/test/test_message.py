
import psimbols.err
import psimbols.message
import unittest

class TestMessage(unittest.TestCase):

    def setUp(self):
        self.processor = psimbols.message.Processor()
        
    def test_channel_message(self):
        im = {'channel': '1234567890', 'request': 'abcdefghijklmnopqrstuvwxyz'}
        om = self.processor.process(im)
        self.assertEqual('got channel request', om['response'])

    def test_public_key_message(self):
        im = {
               'public_key': {
                 'type': 'RSA',
                 'data': '1234567890'
                },
               'request': 'abcdefghijklmnopqrstuvwxyz'
             }
        om = self.processor.process(im)
        self.assertEqual('got channel setup', om['response'])

    def test_no_request_on_channel(self):
        im = {'channel': '0987654321'}
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)

    def test_no_request_on_public_key(self):
        im = {
               'public_key': {
                 'type': 'RSA',
                 'data': '1234567890'
                }
             }
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)

    def test_no_client_identifier(self):
        im = {'request': '0987654321'}
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)

    def test_bad_client_identifier(self):
        im = {'someone': '123', 'request': '0987654321'}
        self.assertRaises(psimbols.err.BadMessageFormat,
                          self.processor.process, im)

if __name__ == '__main__':
    unittest.main()
